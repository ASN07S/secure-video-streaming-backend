import hmac, hashlib, time, base64

SECRET = b"supersecretkey"

def generate_signed_url(filename, user_id="user123", expiry=300):
    expiry_time = int(time.time()) + expiry
    message = f"{filename}:{user_id}:{expiry_time}".encode()

    signature = hmac.new(SECRET, message, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(signature).decode()

    return {
        "file": filename,
        "user_id": user_id,
        "expiry": expiry_time,
        "signature": token
    }

def verify_signature(file, user_id, expiry, signature):
    if int(time.time()) > int(expiry):
        return False

    message = f"{file}:{user_id}:{expiry}".encode()
    expected = hmac.new(SECRET, message, hashlib.sha256).digest()
    expected_token = base64.urlsafe_b64encode(expected).decode()

    return hmac.compare_digest(expected_token, signature)