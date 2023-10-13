# Note that these imports could have been performed in the __init__.py
# file, but this would make the loading of moviepy slower.

import os
import sys

# Downloads ffmpeg if it isn't already installed
import imageio

# Checks to see if the user has set a place for their own version of ffmpeg

if os.getenv('FFMPEG_BINARY') is None:
    if sys.version_info < (3, 4):
        # uses an old version of imageio with ffmpeg.download.
        imageio.plugins.ffmpeg.download()

# Hide the welcome message from pygame: https://github.com/pygame/pygame/issues/542
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# Clips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.downloader import download_webfile
from moviepy.video.VideoClip import VideoClip, ImageClip, ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, clips_array
from moviepy.video.compositing.concatenate import concatenate_videoclips, concatenate  # concatenate=deprecated

from moviepy.audio.AudioClip import AudioClip, CompositeAudioClip, concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip

# FX

import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import moviepy.video.compositing.transitions as transfx

# Tools

import moviepy.video.tools as videotools
import moviepy.video.io.ffmpeg_tools as ffmpeg_tools
from moviepy.video.io.html_tools import ipython_display
from moviepy.tools import cvsecs

try:
    from .video.io.sliders import sliders
except ImportError:
    pass

# adds easy ipython integration
VideoClip.ipython_display = ipython_display
AudioClip.ipython_display = ipython_display
# -----------------------------------------------------------------
# Previews: try to import pygame, else make methods which raise
# exceptions saying to install PyGame


# Add methods preview and show (only if pygame installed)
try:
    from moviepy.video.io.preview import show, preview
except ImportError:
    def preview(self, *args, **kwargs):
        """NOT AVAILABLE : clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")


    def show(self, *args, **kwargs):
        """NOT AVAILABLE : clip.show requires Pygame installed."""
        raise ImportError("clip.show requires Pygame installed")

VideoClip.preview = preview
VideoClip.show = show

try:
    from moviepy.audio.io.preview import preview
except ImportError:
    def preview(self, *args, **kwargs):
        """ NOT AVAILABLE : clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")

AudioClip.preview = preview
