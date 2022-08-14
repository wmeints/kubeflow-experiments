from os import path, mkdir
from pathlib import Path

import argparse
from minio import Minio


def download_file(client, bucket, bucket_path, output_file):
    print(f"Downloading {bucket_path} from bucket {bucket}")

    response = client.get_object(bucket, bucket_path)

    with open(output_file, "wb") as f:
        for chunk in response.stream(512):
            f.write(chunk)

    print(f"Done downloading file. Stored in {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Download files from minio")

    parser.add_argument("--host", type=str, help="Host name of the minio server", default="minio-service.kubeflow.svc.cluster.local")
    parser.add_argument("--port", type=int, help="Port to connect to on the minio server", default=9000)
    parser.add_argument("--secure", type=bool, help="Flag indicating that a TLS connection is required", default=False)
    parser.add_argument("--access-key", type=str, help="Access key (user name) to use", default="minio")
    parser.add_argument("--secret-key", type=str, help="Secret key (password) to use", default="minio123")
    parser.add_argument("--bucket", type=str, help="Bucket to load the data from")
    parser.add_argument("--path", type=str, help="The path in the bucket to load the data from")
    parser.add_argument("--output", type=str, help="The output path where to store the file")

    args = parser.parse_args()

    client = Minio(
        endpoint=f"{args.host}:{args.port}",
        secure=args.secure,
        access_key=args.access_key,
        secret_key=args.secret_key,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    download_file(client, args.bucket, args.path, args.output)


if __name__ == "__main__":
    main()
