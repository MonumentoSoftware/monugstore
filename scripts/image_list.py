
from monugstore import GCSManager

if __name__ == '__main__':
    gcs = GCSManager.from_json_string('GOOGLE_APPLICATION_CREDENTIALS')
    bucket = gcs.create_bucket('image-guru')
    files = bucket.list_blobs()
