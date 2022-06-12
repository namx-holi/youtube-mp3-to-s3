
import requests


_YT_API_VERSION = "v3"
_YT_API_BASE_URL = f"https://www.googleapis.com/youtube/{_YT_API_VERSION}"


class YoutubeAPI:

	def __init__(self, api_key):
		self.api_key = api_key


	def _make_request(self, url, params):
		# Add API key to the request. Make a copy so that request
		#  doesn't update the actual params given.
		params = params.copy()
		params.update({"key": self.api_key})

		r = requests.get(url=url, params=params)

		# TODO: Handle exceptions if json isn't returned
		r_json = r.json()

		if r_json.get("error") != None:
			print(f"ERROR {r_json['error']['code']}: {r_json['error']['message']}")

		return r_json


	def get_playlist_items(self, playlist_id):
		# https://developers.google.com/youtube/v3/docs/playlistItems/list
		url = f"{_YT_API_BASE_URL}/playlistItems"

		params = {
			"part": "id,snippet",
			"playlistId": playlist_id,
			"maxResults": 50
		}

		# Used for pagination. Set as something so the loop can start.
		next_page_token = ""

		videos = []
		while next_page_token is not None:
			resp = self._make_request(url=url, params=params)

			# Get videos from response
			videos += resp.get("items", [])
			
			# Handle pagination
			next_page_token = resp.get("nextPageToken")
			params.update({"pageToken": next_page_token})

		return videos
