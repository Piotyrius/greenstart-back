"""
Company Logo Uploader

Uploads company logos to Google Cloud Storage for B2B buyers.
"""
import os
from django.conf import settings
from google.cloud import storage
from PIL import Image
import io


def upload_company_logo(file, buyer_id, company_name):
    """
    Upload company logo to Google Cloud Storage.
    
    Args:
        file: Uploaded file object (Django UploadedFile)
        buyer_id: Buyer ID
        company_name: Company name for filename
        
    Returns:
        str: Public URL of uploaded logo
    """
    bucket_name = getattr(settings, 'GS_BUCKET_NAME', 'greweco-certificates')
    
    try:
        # Validate image
        img = Image.open(file)
        img.verify()
        
        # Reset file pointer
        file.seek(0)
        
        # Resize if too large (max 500x500)
        img = Image.open(file)
        if img.width > 500 or img.height > 500:
            img.thumbnail((500, 500), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            file = buffer
        
        # Initialize Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Create blob name (sanitize company name)
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_company_name = safe_company_name.replace(' ', '_')
        blob_name = f"logos/b2b_{buyer_id}_{safe_company_name}.png"
        
        blob = bucket.blob(blob_name)
        
        # Upload file
        blob.upload_from_file(file, content_type='image/png')
        blob.make_public()
        
        # Return public URL
        return blob.public_url
    except Exception as e:
        # Fallback: save locally if GCS fails (for development)
        if settings.DEBUG:
            local_path = f"media/logos/b2b_{buyer_id}_{company_name}.png"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                if hasattr(file, 'read'):
                    f.write(file.read())
                else:
                    file.seek(0)
                    f.write(file.getvalue())
            return f"/{local_path}"
        else:
            raise Exception(f"Failed to upload logo to GCS: {str(e)}")

