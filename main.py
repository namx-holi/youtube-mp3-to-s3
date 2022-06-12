
from config import Config
from s3_uploader import S3Uploader
from youtube_api import YoutubeAPI
from youtubedl_api import YoutubeDLAPI



class PlaylistDownloader:
	"""
	Takes a playlist and downloads it, then returns the filepaths.
	"""

	def __init__(self, yt_api, ytdl_api):
		self.yt_api = yt_api
		self.ytdl_api = ytdl_api


	def download_playlist(self, playlist_tag):
		videos = self.yt_api.get_playlist_items(playlist_tag)

		# Reconstruct the videos list into a form we can actually use
		videos = [
			(v["snippet"]["videoOwnerChannelTitle"], # Video author
			v["snippet"]["title"], # Video title
			v["snippet"]["resourceId"]["videoId"]) # Video url
			for v in videos]

		# Pass to ytdl and process
		self.ytdl_api.add_videos_to_queue(videos)
		filepaths = self.ytdl_api.process()

		# Return filepaths to then be handled by S3 uploader
		return filepaths



# Set up APIs
youtube_api = YoutubeAPI(Config.YOUTUBE_API_KEY)
youtubedl_api = YoutubeDLAPI("downloaded_videos")

# Download this playlist
playlist_tag = "PLC4pl84M6cN1JrVEtWTTIVUmgJl52Ql4h"
downloader = PlaylistDownloader(youtube_api, youtubedl_api)
filepaths = downloader.download_playlist(playlist_tag)

# Upload the playlist to S3
uploader = S3Uploader()
uploader.add_files(filepaths)
uploader.set_credentials(
	aws_access_key=Config.AWS_ACCESS_KEY,
	aws_secret_key=Config.AWS_SECRET_KEY)
uploader.upload(
	bucket_name=Config.S3_BUCKET_NAME,
	bucket_directory=Config.S3_STORE_PATH,
	s3_region_name=Config.S3_REGION_NAME)
