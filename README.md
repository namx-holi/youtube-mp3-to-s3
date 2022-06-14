# youtube-mp3-to-s3
Downloads videos from youtube using youtube-dl, then converts them to mp3 using moviepy and uploads them to a specified S3 bucket


## Setup
(Optional) Create a virtual environment

Install requirements using `pip install -r requirements.txt`

Set up environment variables:
	- AWS_ACCESS_KEY  = Your AWS access key id
	- AWS_SECRET_KEY  = Your AWS secret key
	- S3_REGION_NAME  = Region of the S3 bucket
	- S3_BUCKET_NAME  = Name of the bucket we are storing MP3s in
	- S3_STORE_PATH   = Path within the S3 bucket to store MP3s
	- YOUTUBE_API_KEY = A youtube API key to retrieve playlist data

Create a folder called `downloaded_videos` if it doesn't exist. This is used to store the downloaded videos, and mp3s once the videos are processed. Note: Videos are not kept after they are processed.

In `main.py`, near the bottom, set the `playlist_tag` variable to your playlist ID and set the `bucket_directory` arg of `uploader.upload` to `Config.S3_STORE_PATH+"/YOUR_PATH` where `YOUR_PATH` is where you want to store the MP3s within the given `S3_STORE_PATH`.


## Running
Just run `py main.py`!


## Notes
We don't use youtube-dl to convert the video to mp3, as that was using ffmpeg and for some reason ffmpeg doesn't update the signature of an mp3 when converting it from something else. This was leading to issues where a file was an mp3, but when downloading that file from the S3 bucket it was interpreted as an mp4 video since the signature was unchanged. Moviepy doesn't have this issue.


## TODO
- Move the playlist ID and store path stuff to somewhere else
- Add functionality for multiple playlist IDs and store paths do batches
- Move the temp directory used to store downloaded MP3s to an env var
