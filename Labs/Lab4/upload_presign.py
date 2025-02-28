import argparse
import boto3
import requests
import os

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded file: {filename}")
    else:
        raise Exception("Failed to download file.")

def upload_to_s3(filename, bucket_name):
    s3 = boto3.client('s3')
    s3.upload_file(filename, bucket_name, os.path.basename(filename))
    print(f"Uploaded {filename} to s3://{bucket_name}/{os.path.basename(filename)}")

def generate_presigned_url(bucket_name, object_name, expires_in):
    s3 = boto3.client('s3')
    response = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expires_in
    )
    return response

def main():
    parser = argparse.ArgumentParser(description="Download, Upload, and Presign an S3 File.")
    parser.add_argument("url", type=str, help="URL of the file to download")
    parser.add_argument("bucket", type=str, help="S3 bucket name")
    parser.add_argument("expires", type=int, help="Presigned URL expiration time in seconds")
    args = parser.parse_args()

    filename = os.path.basename(args.url)
    download_file(args.url, filename)
    upload_to_s3(filename, args.bucket)
    presigned_url = generate_presigned_url(args.bucket, filename, args.expires)

    print(f"Presigned URL: {presigned_url}")

if __name__ == "__main__":
    main()