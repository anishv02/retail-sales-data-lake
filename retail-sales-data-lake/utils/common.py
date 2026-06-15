from datetime import datetime
import uuid


def generate_batch_id():
    return str(uuid.uuid4())


def current_timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")