import os
from pathlib import Path
import sys 

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from configs.config import (
    BUCKET_NAME,
    RAW_PREFIX,
    SOURCE_SYSTEM
)

from utils.common import (
    generate_batch_id,
    current_timestamp
)

from utils.s3_helper import get_s3_client 

def ingest_file(local_file_path):
    batch_id = generate_batch_id()
    timestamp = current_timestamp()

    file_name = os.path.basename(local_file_path)

    s3_key = (
        f"{RAW_PREFIX}/"
        f"{SOURCE_SYSTEM}/"
        f"{timestamp}/"
        f"{file_name}"
    )

    s3 = get_s3_client()

    s3.upload_file(
        local_file_path,
        BUCKET_NAME,
        s3_key
    )

    print("Uploaded successfully")
    print(f"Batch ID: {batch_id}")
    print(f"S3 Key: {s3_key}")
    
    return {
        "batch_id": batch_id,
        "s3_key": s3_key
    }

if __name__ == "__main__":
    # Example usage
    local_file_path = "data/source/retail_sales.csv"
    ingest_file(local_file_path)

