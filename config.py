
import os

class Config:

	# S3 bucket config
	AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
	AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
	S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

	# Youtube Data API config
	YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
