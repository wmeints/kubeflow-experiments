from os import path, stat
from pathlib import Path

import argparse
from minio import Minio


def upload_file(client, bucket, bucket_path, input_file):  
    file_stats = stat(input_file)

    with open(input_file, "rb") as f:
        client.put_object(bucket, bucket_path, f, file_stats.st_size)


def main():
    parser = argparse.ArgumentParser(description="Download files from minio")

    parser.add_argument("--host", type=str, help="Host name of the minio server", default="minio-service.kubeflow.svc.cluster.local")
    parser.add_argument("--port", type=int, help="Port to connect to on the minio server", default=9000)
    parser.add_argument("--secure", type=bool, help="Flag indicating that a TLS connection is required", default=False)
    parser.add_argument("--access-key", type=str, help="Access key (user name) to use", default="minio")
    parser.add_argument("--secret-key", type=str, help="Secret key (password) to use", default="minio123")
    parser.add_argument("--bucket", type=str, help="Bucket to upload the data to")
    parser.add_argument("--path", type=str, help="The path in the bucket to upload the data to")
    parser.add_argument("--input", type=str, help="The input path where to load from")

    args = parser.parse_args()

    client = Minio(
        endpoint=f"{args.host}:{args.port}",
        secure=args.secure,
        access_key=args.access_key,
        secret_key=args.secret_key,
    )

    upload_file(client, args.bucket, args.path, args.input)


if __name__ == "__main__":
    main()
