from flask import Blueprint, request, jsonify, abort, current_app
from app.services.token_service import generate_signed_url, verify_signature
from app.services.streaming_service import stream_video
from app.services.rate_limiter import is_allowed
from app.services.replay_protection import is_token_used, mark_token_used
from app.utils.logger import log_request
import os

video_bp = Blueprint("video", __name__)

# Fake DB for ownership
VIDEO_OWNERS = {
    "sample.mp4": "user123"
}

FAILED_ATTEMPTS = {}

def track_fail(ip):
    FAILED_ATTEMPTS[ip] = FAILED_ATTEMPTS.get(ip, 0) + 1


@video_bp.route("/")
def home():
    return {"message": "Secure Video Streaming API Running"}


@video_bp.route("/get-video")
def get_video():
    file = request.args.get("file")
    user_id = request.args.get("user_id", "user123")

    return jsonify(generate_signed_url(file, user_id))


@video_bp.route("/stream")
def stream():
    ip = request.remote_addr

    if not is_allowed(ip):
        return jsonify({"error": "Too many requests"}), 429

    file = request.args.get("file")
    user_id = request.args.get("user_id")
    expiry = request.args.get("expiry")
    signature = request.args.get("signature")

    if not verify_signature(file, user_id, expiry, signature):
        track_fail(ip)
        abort(403)

    # Replay protection
    if is_token_used(signature):
        track_fail(ip)
        return jsonify({"error": "Replay attack detected"}), 403

    mark_token_used(signature)

    # Access control
    if VIDEO_OWNERS.get(file) != user_id:
        track_fail(ip)
        return jsonify({"error": "Unauthorized access"}), 403

    path = os.path.join(current_app.config["VIDEO_FOLDER"], file)

    if not os.path.exists(path):
        abort(404)

    response = stream_video(path)

    log_request(ip, request.path, response.status_code)

    return response