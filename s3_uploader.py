
import boto3
import os.path
from botocore.exceptions import ClientError
from tqdm import tqdm



class S3Uploader:

	def __init__(self):
		self.aws_access_key = None
		self.aws_secret_key = None

		self.files_to_upload = []


	def set_credentials(self, aws_access_key, aws_secret_key):
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key


	def add_file(self, filepath):
		self.files_to_upload.append(filepath)


	def add_files(self, filepaths):
		return [self.add_file(f) for f in filepaths]


	def upload(self, bucket_name, bucket_directory, s3_region_name=None):
		bucket = self._get_s3_bucket(bucket_name, s3_region_name)

		with tqdm(total=len(self.files_to_upload)) as main_pbar:
			while len(self.files_to_upload) != 0:
				filepath = self.files_to_upload.pop(0)

				# Construct the key for S3 (basically save path)
				filename = os.path.basename(filepath)
				s3_key = f"{bucket_directory}/{filename}"

				# Get the file size for tqdm progress bar
				filesize = os.path.getsize(filepath)

				# Create a pbar that can be updated using upload_fileObj callback
				file_pbar = tqdm(
					total=filesize,
					unit="iB",
					unit_scale=True,
					unit_divisor=1024,
					leave=False)
				callback = lambda b: file_pbar.update(b)

				# Actually open the file and upload!
				with open(filepath, "rb") as fileobj:
					bucket.upload_fileobj(
						Fileobj=fileobj,
						Key=s3_key,
						Callback=callback,
						ExtraArgs={
							"ContentType": "audio/mpeg",
							"ACL": "public-read"})

				# Close the file pbar, and update the main pbar counting files
				file_pbar.close()
				main_pbar.update(1)


	def _get_s3_bucket(self, bucket_name, s3_region_name):
		if not self.aws_access_key or not self.aws_secret_key:
			# Try use default config
			print("Starting AWS session using default config")
			session = boto3.session.Session()

		else:
			# Use keys set in config.py
			print("Starting AWS session using config from environment vars")
			session = boto3.session.Session(
				aws_access_key_id=self.aws_access_key,
				aws_secret_access_key=self.aws_secret_key,
				region_name=s3_region_name)

		print(session.available_profiles)

		s3 = session.resource("s3")
		bucket = s3.Bucket(bucket_name)
		return bucket
