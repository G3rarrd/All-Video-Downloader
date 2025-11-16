from pathlib import Path
from platformdirs import user_downloads_dir
import os
import subprocess
from typing import Any
from yt_dlp import YoutubeDL
from yt_dlp.utils import UnsupportedError, DownloadError 
from collections import defaultdict
import re
import json


class AllVideoDownloader:
    """ 
    An all you can download video downloader that extracts, analyzes, and downloads videos 
    from various platforms with format selection and post processing
    
    Features:
    - Multi-platform video downloading (YouTube(best), Instagram, TikTok, etc)
    - Video and audio Format analysis and combination
    - Automatic aspect ratio correction for vertical videos using ffmpeg
    - Metadata extraction such as title, view count, like count if available
    - File size estimation and format filtering 
    """
    def __init__(self, video_url : str):
        """
            Inititalize the video downloader with chosen video URL.

            Args: 
                url (str): The video URL to download from supported websites
        """
        self.video_url : str = video_url
        # print(user_downloads_dir())
        self.download_dir = Path(user_downloads_dir())


        self.info = None
        self.video_formats : list[dict[str, Any]] = []
        self.audio_formats : list[dict[str, Any]] = []
        self.video_audio_formats : list[tuple[dict[str, Any], dict[str, Any]]] = []

        self.view_count : int = 0
        self.domain : str = ""
        self.title : str = ""
        self.duration : int = 0
        self.like_count : int = 0
        self.uploader_name : str = ""
        self.platform : str = ""

        self.illegal_chars = r'[<>:"/\\|?*\n]'
        
        #
        self.fetch_info()
        self.parse_formats()

    def fetch_info(self):
        """ Retrieve video metadata without downloading content """

        ydl_opts = {
            'quiet' : False,
            "listformats": True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                self.info = ydl.extract_info(self.video_url, download=False)
                self.display_video_info()
                

        except UnsupportedError:
            print(f"Unsupported URL: {self.video_url}")
            self.info = None
            self.title = "Unknown Title"

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.info = None
            self.title = 'Unknown Title'


    def set_info(self):
        self.title = self.info.get('title', 'Unknown Title')
        self.domain = self.info.get('webpage_url_domain', 'N/A')
        self.duration = self.info.get('duration', 0)
        self.like_count = self.info.get('like_count', 0)
        self.uploader_name = self.info.get('uploader', 'N/A')
        self.platform = self.info.get('extractor_key', 'N/A')
        self.view_count = self.info.get("view_count", 0)
        

    def display_video_info(self):
        """ Displays the video metadata """

        self.set_info()
        duration = self.info.get("duration_string", "00:00:00")

        print(f"""
            ╔════════════════════════════════════════╗
            🎬 Title:     {self.title}
            💻 Platform:  {self.platform}
            👤 Uploader:  {self.uploader_name}
            ⏱️ Duration:  {duration}
            🔎 Views:     {self.view_count}
            ❤️ Likes:     {self.like_count}
            ╚════════════════════════════════════════╝
            """)
        

    def clean_filename(self, title: str):
        """ Cleans up title of the video url to be used as a filename """
        MAX_LENGTH: int = 127
        safe = re.sub(r'[<>:"/\\|?*\n#~·]', '', title)
        safe = re.sub(r'\s+', ' ', safe).strip()

        if len(safe) > MAX_LENGTH:
            safe = f"{safe[:MAX_LENGTH]}..."
        
        return safe

    def display_all_metadata(self) -> str:
        return json.dumps(self.info, indent=2)

    def get_file_size(self, format: dict) -> float:
        """ Get the size of the format """
        return (format.get("filesize") or 0) / (1024**2)

    def filter_ext(self, ext:str, formats:list):
        """Filter out the specified ext (mp4, webm, m4a)"""
        return [ f for f in formats if (f.get('ext') or '') != ext]

    def parse_formats(self):
        """ Separate and Sort audio and video formats if they exist"""
        formats = self.info.get("formats", [])

        # Extract Video Formats and Remove Duplicates
        self.video_formats = [
            f for f in formats 
            if f.get('acodec') == 'none' and 
            f.get('vcodec') != 'none']
        
        self.video_formats = self.filter_ext('webm', self.video_formats)
        self.video_formats = self.clean_video_formats()
        self.video_formats.sort(key=lambda f : ((f.get('height') or 0),  (f.get('tbr') or 0)), reverse=True)

        # Extract Audio Formats
        self.audio_formats = [ 
            f for f in formats 
            if f.get('acodec') != 'none' and 
            f.get('vcodec') == 'none' and 
            (f.get("language") is None or str(f.get("language", "en")).startswith("en"))]
        
        # print(len(self.audio_formats))
        self.audio_formats = self.filter_ext('webm', self.audio_formats)
        self.audio_formats.sort(key=lambda f : (f.get('abr') or 0), reverse=True)

        self.combine_video_audio()

        # No separate audio and video was found
        if len(self.video_audio_formats) == 0:
            self.video_formats = [f for f in formats]
        
        self.video_formats = self.clean_video_formats()
        self.video_formats.sort(key=lambda f : ((f.get('height') or 0),  (f.get('tbr') or 0)), reverse=True)


    def clean_video_formats(self): 
        """  Remove Duplicates and get the best format of each height and ext """
        unique = defaultdict(str)
        for f in self.video_formats:
            key = str(f.get('height')) + f.get("ext") # Height and ext of the format
            unique[key] = f

        return list(unique.values())
    
    
    def combine_video_audio(self):
        """ Combine both video and audio formats to their respective file extensions (ext) """
        for v_f in self.video_formats:
            v_ext = v_f.get('ext')

            for a_f in self.audio_formats:
                a_ext = a_f.get('ext')

                if ((v_ext == 'mp4' and a_ext in ['m4a', 'mp4']) or
                    (v_ext == 'webm' and a_ext == 'webm')):
                    join : tuple[dict[str, Any], dict[str, Any]] = (v_f, a_f)
                    self.video_audio_formats.append(join)
                    break 


    def display_video_audio_format_info(self):
        """ Displays the video formats and audio Streams available in the video url """

        print("Video Download(s): ")
        if  len(self.video_audio_formats) == 0:
            for index, f in enumerate(self.video_formats):
                resolution : str = f"{f.get('height')}p"
                fps : str = f"{f.get('fps', "N/A")}"
                v_ext = f.get('ext', "N/A")
                total_size = self.get_file_size(f)
                file_size_text: str = f"{total_size:.3f} MiB" if total_size > 0 else "N/A"
                print(f"🔹 ID: {str(index + 1):<2} | {resolution:<5} | Video: {v_ext:<4} | {fps} | Size: {file_size_text:<7}")
            return

        for index, v_a_f in enumerate(self.video_audio_formats):
            v_f : dict[str, Any] = v_a_f[0]
            a_f : dict[str, Any] = v_a_f[1]

            resolution : str = f"{v_f.get('height')}p"
            fps : str = f"{v_f.get('fps', "N/A")}"
            v_ext = v_f.get('ext', "N/A")
            a_ext = a_f.get('ext', "N/A")
            total_size = self.get_file_size(v_f) + self.get_file_size(a_f)
            file_size_text: str = f"{total_size:.3f} MiB" if total_size > 0 else "N/A"

            print(f"🔹 ID: {str(index + 1):<2} | {resolution:<5} | Video: {v_ext:<4} + Audio: {a_ext:<4} | {fps} | Size: {file_size_text:<7}")



    def fix_aspect_ratio(self, input_file: str):
        """ 
        Automatically corrects the video aspect ratio for vertical videos

        Args:
            input_file(str): This is the file directory of the downloaded video
        """

        temp_file = input_file + "_fixed.mp4"
        command = [
            "ffmpeg",
            '-y', # overwrite
            "-i", input_file,
            "-preset", "fast",
            '-metadata:s:v', 'rotate=0',
            "-c:a", "aac",
            temp_file
        ]

        subprocess.run(command, check=True)
        os.replace(temp_file, input_file)


    def download(self, id: int):
        """ 
        Download selected video format with combined Audio streams 

        Args:
            id: Format identifier from display list (1-based indexing)
        
        Raises:
            IndexError: If provided ID is not within range
            DownloadError: If yt-dlp fails to download the video
        
        """

        filename = self.clean_filename(self.title)
        format_code : str = ""
        height: int = 0
        width : int = 0 


        if len(self.video_audio_formats) > 0:
            video: dict[str, Any] = self.video_audio_formats[id - 1][0]
            audio : dict[str, Any]= self.video_audio_formats[id - 1][1]

            format_code = f"{video.get('format_id')}+{audio.get('format_id')}"
            height  = video.get("height", 0)
            width = video.get("width", 0)
            
        else:
            # Video URL does not contain standalone audio
            video: dict[str, Any] = self.video_formats[id - 1]
            format_code = f"{video.get('format_id')}"
            height = video.get("height", 0)
            wdith = video.get("width", 0)


        output_template = self.download_dir / f'{filename}.%(ext)s'

        ydl_opts = {
            'format' : format_code,
            'outtmpl': str(output_template),
            'list-formats' : True
        }
        try :
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_url])

        except DownloadError as e:
            print (f"Download Error:{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}") 

        if (width < height): 
            ext = self.info.get("ext", "mp4")
            file_dir = str(self.download_dir / Path(f"{filename}.{ext}"))
            self.fix_aspect_ratio(file_dir)



