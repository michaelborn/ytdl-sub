import json
import os
from pathlib import Path
from typing import List

from yt_dlp.utils import RejectedVideoReached

from ytdl_subscribe.downloaders.downloader import Downloader
from ytdl_subscribe.entries.youtube import YoutubeVideo


class YoutubeDownloader(Downloader):
    """
    Class that handles downloading youtube entries via ytdl and converting them into
    YoutubeVideo objects
    """

    @classmethod
    def playlist_url(cls, playlist_id: str) -> str:
        """Returns full playlist url"""
        return f"https://youtube.com/playlist?list={playlist_id}"

    @classmethod
    def video_url(cls, video_id: str) -> str:
        """Returns full video url"""
        return f"https://youtube.com/watch?v={video_id}"

    @classmethod
    def channel_url(cls, channel_id: str) -> str:
        """Returns full channel url"""
        return f"https://youtube.com/channel/{channel_id}"

    def _download_with_metadata(self, url: str) -> None:
        """
        Do not get entries from the extract info, let it write to the info.json file and load
        that instead. This is because if the video is already downloaded in a playlist, it will
        not fetch the metadata (maybe there is a way??)
        """
        ytdl_metadata_override = {
            "writeinfojson": True,
        }

        try:
            _ = self.extract_info(ytdl_options_overrides=ytdl_metadata_override, url=url)
        except RejectedVideoReached:
            pass

    def download_video(self, video_id: str) -> YoutubeVideo:
        """Download a single Youtube video"""
        entry = self.extract_info(url=self.video_url(video_id))
        return YoutubeVideo(**entry)

    def download_playlist(self, playlist_id: str) -> List[YoutubeVideo]:
        """
        Downloads all videos in a Youtube playlist
        """
        playlist_url = self.playlist_url(playlist_id=playlist_id)

        self._download_with_metadata(url=playlist_url)

        # Load the entries from info.json, ignore the playlist entry
        entries: List[YoutubeVideo] = []

        # Load the entries from info.json, ignore the playlist entry
        for file_name in os.listdir(self.output_directory):
            if file_name.endswith(".info.json") and not file_name.startswith(playlist_id):
                with open(Path(self.output_directory) / file_name, "r", encoding="utf-8") as file:
                    entries.append(YoutubeVideo(**json.load(file)))

        return entries

    def download_channel(self, channel_id: str) -> List[YoutubeVideo]:
        """
        Downloads all videos from a channel
        TODO: Add caching via ids in the metadata. Scrape output directory for any vid ids and
        TODO: include it in the archive
        """
        self._download_with_metadata(url=self.channel_url(channel_id))

        # Load the entries from info.json
        entries: List[YoutubeVideo] = []

        # Load the entries from info.json
        # TODO dupe code between this and playlist
        for file_name in os.listdir(self.output_directory):
            if file_name.endswith(".info.json") and not file_name.startswith(channel_id):
                with open(Path(self.output_directory) / file_name, "r", encoding="utf-8") as file:
                    entries.append(YoutubeVideo(**json.load(file)))

        return entries
