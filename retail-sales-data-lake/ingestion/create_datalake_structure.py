import sys
from pathlib import Path
# ensure project root is on sys.path so sibling packages like `utils` can be imported
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from utils.s3_helper import get_s3_client
BUCKET_NAME = 'test-demo-343218219833-ap-south-1-an'

FOLDERS = [
    "raw/sales/",
    "validated/sales/",
    "curated/sales/",
    "analytics/sales_summary/",
    "audit/validation_results/",
    "rejected/sales/"
]

def create_folders():
    s3 = get_s3_client()

    for folder in FOLDERS:
        s3.put_object(
            Bucket = BUCKET_NAME,
            Key = folder
        )
        print(f"Created: {folder}")

if __name__ == "__main__":
    create_folders()