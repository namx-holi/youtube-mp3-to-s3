
import os

class Config:

	# AWS config
	AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
	AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

	# S3 config
	S3_REGION_NAME = os.environ.get("S3_REGION_NAME")
	S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
	S3_STORE_PATH  = os.environ.get("S3_STORE_PATH")

	# Youtube Data API config
	YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
