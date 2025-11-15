"""
PDF Certificate Generator

Generates PDF certificates for NFT tree ownership with CO₂ absorption data.
Uploads to Google Cloud Storage and returns public URL.
"""
import os
import io
import qrcode
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfgen import canvas
from django.conf import settings
from google.cloud import storage

# Logo colors from design system
PRIMARY_GREEN = colors.HexColor('#2D5016')
SECONDARY_GREEN = colors.HexColor('#4A7C2E')
LIGHT_GREEN = colors.HexColor('#6BA84F')
GREY = colors.HexColor('#808080')


def generate_qr_code(data):
    """Generate QR code image from data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer


def generate_certificate_pdf(nft_certificate):
    """
    Generate PDF certificate for NFT tree ownership.
    
    Args:
        nft_certificate: NFTCertificate instance
        
    Returns:
        str: Public URL of uploaded PDF
    """
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY_GREEN,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY_GREEN,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=10,
        alignment=TA_LEFT
    )
    
    # Title
    elements.append(Paragraph("NFT Tree Ownership Certificate", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Certificate details
    purchase = nft_certificate.purchase
    buyer = purchase.buyer
    tree_lot = purchase.tree_lot
    plantation = tree_lot.plantation
    
    # Certificate info table
    cert_data = [
        ['Certificate ID:', f'#{nft_certificate.id}'],
        ['NFT Token ID:', nft_certificate.nft_token_id or 'Not Minted Yet'],
        ['Issue Date:', nft_certificate.issued_at.strftime('%B %d, %Y')],
        ['', ''],
    ]
    
    cert_table = Table(cert_data, colWidths=[2*inch, 4*inch])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GREEN),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(cert_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Buyer details
    elements.append(Paragraph("Buyer Information", heading_style))
    
    # Add company logo for B2B buyers
    if buyer.buyer_type == 'b2b' and buyer.company_logo:
        try:
            from reportlab.lib.utils import ImageReader
            import requests
            logo_response = requests.get(buyer.company_logo, timeout=5)
            if logo_response.status_code == 200:
                logo_img = Image(ImageReader(io.BytesIO(logo_response.content)), width=2*inch, height=0.5*inch)
                elements.append(logo_img)
                elements.append(Spacer(1, 0.1*inch))
        except Exception:
            pass  # Skip logo if can't load
    
    buyer_data = [
        ['Buyer Type:', buyer.get_buyer_type_display()],
        ['Contact:', buyer.name],
        ['Email:', buyer.email],
    ]
    
    if buyer.buyer_type == 'b2b':
        buyer_data.extend([
            ['Company Name:', buyer.company_name or 'N/A'],
            ['Country:', buyer.country or 'N/A'],
            ['Website:', buyer.website or 'N/A'],
        ])
    else:
        buyer_data.extend([
            ['Phone:', buyer.phone or 'N/A'],
            ['Address:', buyer.address or 'N/A'],
        ])
    
    buyer_table = Table(buyer_data, colWidths=[2*inch, 4*inch])
    buyer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ]))
    elements.append(buyer_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Purchase details
    elements.append(Paragraph("Purchase Details", heading_style))
    purchase_data = [
        ['Trees Purchased:', f'{purchase.quantity} trees'],
        ['Total Price:', f'${purchase.total_price}'],
        ['Purchase Date:', purchase.purchase_date.strftime('%B %d, %Y')],
        ['Payment Reference:', purchase.payment_reference or 'N/A'],
    ]
    
    purchase_table = Table(purchase_data, colWidths=[2*inch, 4*inch])
    purchase_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ]))
    elements.append(purchase_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Plantation details
    elements.append(Paragraph("Plantation Details", heading_style))
    plantation_data = [
        ['Plantation Name:', plantation.name],
        ['Species:', plantation.species],
        ['Planting Date:', plantation.planting_date.strftime('%B %d, %Y')],
        ['Tree Lot:', tree_lot.lot_number],
        ['Area:', f'{tree_lot.area_hectares} hectares'],
    ]
    
    plantation_table = Table(plantation_data, colWidths=[2*inch, 4*inch])
    plantation_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ]))
    elements.append(plantation_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # CO₂ Absorption - Highlighted section
    elements.append(Paragraph("CO₂ Absorption", heading_style))
    co2_data = [
        ['Total CO₂ Absorbed:', f'{nft_certificate.co2_absorbed_kg:.2f} kg'],
    ]
    
    co2_table = Table(co2_data, colWidths=[2*inch, 4*inch])
    co2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY_GREEN),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(co2_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Note about calculation
    note_text = "Note: CO₂ absorption calculations use placeholder formulas. " \
                "Values will be updated with real biomass-based data in future iterations."
    elements.append(Paragraph(note_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ISO Standards (if any)
    iso_records = nft_certificate.iso_records.all()
    if iso_records.exists():
        elements.append(Paragraph("ISO Compliance", heading_style))
        iso_data = []
        for record in iso_records:
            iso_data.append([f'{record.iso_standard}:', record.get_compliance_status_display()])
        
        iso_table = Table(iso_data, colWidths=[2*inch, 4*inch])
        iso_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, GREY),
        ]))
        elements.append(iso_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # QR Code
    if nft_certificate.qr_code:
        qr_data = nft_certificate.qr_code
    else:
        # Generate QR code data if not exists
        qr_data = f"GREWECO-NFT-{nft_certificate.id}"
        nft_certificate.qr_code = qr_data
        nft_certificate.save(update_fields=['qr_code'])
    
    qr_img_buffer = generate_qr_code(qr_data)
    qr_image = Image(qr_img_buffer, width=1.5*inch, height=1.5*inch)
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Certificate Verification QR Code", heading_style))
    elements.append(qr_image)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Upload to Google Cloud Storage
    pdf_url = upload_to_gcs(buffer, nft_certificate)
    
    return pdf_url


def upload_to_gcs(buffer, nft_certificate):
    """
    Upload PDF to Google Cloud Storage.
    
    Args:
        buffer: BytesIO buffer containing PDF
        nft_certificate: NFTCertificate instance
        
    Returns:
        str: Public URL of uploaded file
    """
    bucket_name = getattr(settings, 'GS_BUCKET_NAME', 'greweco-certificates')
    
    try:
        # Initialize Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Create blob name
        blob_name = f"certificates/nft_{nft_certificate.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        blob = bucket.blob(blob_name)
        
        # Upload file
        blob.upload_from_file(buffer, content_type='application/pdf')
        blob.make_public()
        
        # Return public URL
        return blob.public_url
    except Exception as e:
        # Fallback: save locally if GCS fails (for development)
        if settings.DEBUG:
            local_path = f"media/certificates/nft_{nft_certificate.id}.pdf"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(buffer.read())
            return f"/{local_path}"
        else:
            raise Exception(f"Failed to upload to GCS: {str(e)}")
