from pathlib import Path
from all_video_downloader import AllVideoDownloader

def main():
    try:
        URL: str = input("Enter URL: ").strip()
        if not URL:
            print("❌ No URL provided")
            return 
        downloader : AllVideoDownloader = AllVideoDownloader(URL)
        downloader.display_video_audio_format_info()

        max_id : int = len(downloader.video_audio_formats) if downloader.video_audio_formats else len(downloader.video_formats)
        if max_id == 0:
            print("❌ No available formats found")
            return
        
        try:
            select_download = int(input("Select ID: "))
            downloader.download(select_download)
            print(f"🎉 Download process completed!")
            print(f"📁 Download saved in: {downloader.download_dir}")
        
        except ValueError:
            print("❌ Please enter a valid number")

        except IndexError as e:
            print(f"❌ {e}")

    except KeyboardInterrupt:
        print("\n⏹️  Download cancelled by user")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if "__main__" == __name__:
    main()