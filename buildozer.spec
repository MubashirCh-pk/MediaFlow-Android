
[app]

title = MediaFlow Downloader

package.name = mediaflow

package.domain = com.mediaflow

source.dir = .

source.include_exts = py,kv,png,jpg,txt

version = 1.0

requirements = python3,kivy,yt-dlp

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 35

android.minapi = 23

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

[buildozer]

log_level = 2

warn_on_root = 1
