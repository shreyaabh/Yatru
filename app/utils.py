import uuid

def code_generator():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code