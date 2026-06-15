from datetime import datetime 

def generate_audit(
        records_read,
        records_passed,
        records_failed,
):
    return {
        "validation_time" : 
            str(datetime.utcnow()),
        "records_read" : records_read,
        "records_passed" : records_passed,
        "records_failed" : records_failed
    }