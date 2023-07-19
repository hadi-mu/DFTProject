from google.cloud import storage


def blob_metadata(bucket_name="intern_test", blob_name=""):
    """Prints out a blob's metadata."""
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Retrieve a blob, and its metadata, from Google Cloud Storage.
    # Note that `get_blob` differs from `Bucket.blob`, which does not
    # make an HTTP request.
    blob = bucket.get_blob(blob_name)

    print(f"Blob: {blob.name}")
