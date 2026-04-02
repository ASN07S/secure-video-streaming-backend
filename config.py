import os

class Config:
    SECRET_KEY = "supersecretkey"
    VIDEO_FOLDER = os.path.join(os.getcwd(), "videos")