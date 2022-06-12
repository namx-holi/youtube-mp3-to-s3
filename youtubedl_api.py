
import queue
import os.path
import youtube_dl
from tqdm import tqdm



class VideoQueueItem:
	def __init__(self, video_author, video_title, video_url):
		self.video_author = video_author
		self.video_url    = video_url
		self.video_title  = video_title



class VideoQueue:
	"""
	Wrapper for whatever we are using to videos to still download
	"""
	def __init__(self):
		self.q = queue.Queue()

		# Total number of things in the queue. This is stored as the
		#  size of a queue is not something that is accessible
		self.q_len = 0


	def __len__(self):
		return self.q_len


	def put(self, video_author, video_title, video_url):
		self.q.put((video_author, video_title, video_url))
		self.q_len += 1


	def get(self) -> VideoQueueItem:
		try:
			video_author, video_title, video_url = self.q.get_nowait()
		except queue.Empty:
			return None

		self.q_len -= 1
		return VideoQueueItem(video_author, video_title, video_url)




class YoutubeDLAPI:

	def __init__(self, target_dir, codec="mp3", quality="5"):
		self.target_dir = target_dir
		self.codec = codec

		# Config for downloader
		self.downloader_options = {
			"quiet": True, # Don't show cmdline output
			"format": "bestaudio/best",
			"postprocessors": [{
				"key": "FFmpegExtractAudio",
				"preferredcodec": codec,
				"preferredquality": quality
			}]}

		# Videos to still download
		self.video_queue = VideoQueue()

		# Errors to report on at the end
		self.error_msgs = []


	def add_videos_to_queue(self, videos):
		return [
			self.add_video_to_queue(video_author, video_title, video_url)
			for video_author, video_title, video_url in videos]


	def add_video_to_queue(self, video_author, video_title, video_url):
		self.video_queue.put(video_author, video_title, video_url)


	def process(self) -> list:
		# Clearing cache to avoid some weird 403 errors
		with youtube_dl.YoutubeDL({"quiet": True}) as ydl:
			ydl.cache.remove()

		filepaths = []

		# Progress bar!
		with tqdm(total=len(self.video_queue)) as pbar:

			# Force a refresh to show the pbar without having to wait
			#  for the first update
			pbar.refresh()

			item = self.video_queue.get()
			while item != None:
				filepath = self._download_audio(item)

				if filepath is not None:
					filepaths.append(filepath)
				pbar.update(1)

				item = self.video_queue.get()

		print("")
		print("Finished! Any errors will be printed below")
		for error_msg in self.error_msgs:
			print(" "+error_msg)

		return filepaths


	def _download_audio(self, item: VideoQueueItem) -> str:
		video_author = item.video_author
		video_title  = item.video_title
		video_url    = item.video_url

		# Construct filepath
		filename = f"{video_author} - {video_title}.{self.codec}"
		save_path = os.path.join(self.target_dir, filename)

		# Check if the file already exists
		if os.path.exists(save_path):
			print(f"Skipping {video_author} - {video_title} ({video_url}): Already exists")
			return save_path

		# Create a progress bar for just this file
		pbar = tqdm(
			unit="iB",
			unit_scale=True,
			unit_divisor=1024,
			leave=False)
		def callback(d):
			if d["status"] == "downloading":
				pbar.total = d["total_bytes"]
				pbar.n = d["downloaded_bytes"]
				pbar.refresh()


		# Create new options with the save path template, and callback
		options = dict(
			self.downloader_options,
			**{"outtmpl": save_path, "progress_hooks": [callback]})

		# Try downloading video!
		try:
			with youtube_dl.YoutubeDL(options) as ydl:
				ydl.download([video_url])
		except youtube_dl.utils.DownloadError as e:
			error_msg_raw = str(e).replace("\n", " ")
			error_msg = f"Error downloading {url}: {error_msg_raw}"
			# print(error_msg)
			self.error_msgs.append(error_msg)
			return None

		pbar.close()
		return save_path
