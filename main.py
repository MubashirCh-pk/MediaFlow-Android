
import os
import threading

import yt_dlp

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform


KV = """
BoxLayout:
    orientation: "vertical"
    padding: "20dp"
    spacing: "15dp"

    canvas.before:
        Color:
            rgba: 0.06, 0.08, 0.13, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "MediaFlow"
        font_size: "30sp"
        bold: True
        size_hint_y: None
        height: "60dp"

    Label:
        text: "Your video downloader"
        font_size: "15sp"
        color: 0.6, 0.7, 0.85, 1
        size_hint_y: None
        height: "30dp"

    Spinner:
        id: platform
        text: "YouTube"
        values: ["YouTube", "Instagram", "TikTok", "Facebook"]
        size_hint_y: None
        height: "50dp"

    TextInput:
        id: url
        hint_text: "Paste video link here"
        multiline: False
        size_hint_y: None
        height: "50dp"

    Spinner:
        id: quality
        text: "1080p"
        values: ["Best Available", "2160p", "1440p",
                 "1080p", "720p", "480p", "360p"]
        size_hint_y: None
        height: "50dp"

    Spinner:
        id: format
        text: "MP4"
        values: ["MP4", "MKV", "WebM"]
        size_hint_y: None
        height: "50dp"

    Button:
        text: "DOWNLOAD VIDEO"
        size_hint_y: None
        height: "55dp"
        background_color: 0.15, 0.4, 0.95, 1
        on_release: app.start_download()

    ProgressBar:
        id: progress
        max: 100
        value: 0
        size_hint_y: None
        height: "20dp"

    Label:
        id: status
        text: "Ready to download"
        size_hint_y: None
        height: "50dp"

    Label:
        text: "MediaFlow Android"
        color: 0.5, 0.5, 0.6, 1
"""


class MediaFlowApp(App):

    def build(self):

        self.title = "MediaFlow"

        return Builder.load_string(KV)

    def start_download(self):

        url = self.root.ids.url.text.strip()

        if not url:

            self.set_status("Please enter a video link.")

            return

        quality = self.root.ids.quality.text

        selected_format = self.root.ids.format.text

        threading.Thread(
            target=self.download_video,
            args=(url, quality, selected_format),
            daemon=True
        ).start()

    def download_video(self, url, quality, selected_format):

        try:

            output_folder = self.user_data_dir

            if quality == "Best Available":

                format_selector = "bestvideo+bestaudio/best"

            else:

                height = int(quality.replace("p", ""))

                format_selector = (
                    f"bestvideo[height<={height}]"
                    f"+bestaudio/"
                    f"best[height<={height}]"
                )

            options = {

                "format": format_selector,

                "outtmpl": os.path.join(
                    output_folder,
                    "%(title)s.%(ext)s"
                ),

                "noplaylist": True,

                "quiet": True,

                "retries": 5,

                "merge_output_format": selected_format.lower(),

                "progress_hooks": [self.progress_hook],

            }

            with yt_dlp.YoutubeDL(options) as downloader:

                downloader.download([url])

            self.set_status(
                "Download completed!"
            )

        except Exception as error:

            self.set_status(
                "Error: " + str(error)[:150]
            )

    def progress_hook(self, data):

        if data["status"] == "downloading":

            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
            )

            downloaded = data.get("downloaded_bytes", 0)

            if total:

                percentage = downloaded / total * 100

                Clock.schedule_once(
                    lambda dt: self.update_progress(
                        percentage
                    )
                )

    def update_progress(self, percentage):

        self.root.ids.progress.value = percentage

        self.root.ids.status.text = (
            f"Downloading: {percentage:.1f}%"
        )

    def set_status(self, message):

        Clock.schedule_once(
            lambda dt: self.update_status(message)
        )

    def update_status(self, message):

        self.root.ids.status.text = message


if __name__ == "__main__":

    MediaFlowApp().run()
