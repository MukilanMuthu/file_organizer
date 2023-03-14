from os.path import splitext, exists, join
from os import scandir, rename
from shutil import move
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

download_dir = "c:\\Users\\mukil\\Downloads"
videos_dir = download_dir + "\\Videos"
music_dir = download_dir + "\\Music"
images_dir = download_dir + "\\Images"
doc_dir = download_dir + "\\Documents"
prog_dir = download_dir + "\\Programs"
comp_dir = download_dir + "\\Compressed"
torr_dir = download_dir + "\\Torrents"

#  supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt",
                    ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
#  supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mkv",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
#  supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
#  supported Document types
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

compressed_extensions = [".7z", ".arj", ".deb", ".pkg", ".rar", ".rpm", ".tar.gz", ".z", ".zip"]


def make_unique(destination, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(destination, entry, name):
    if exists(f"{destination}/{name}"):
        unique_name = make_unique(destination, name)
        oldName = join(destination, name)
        newName = join(destination, unique_name)
        rename(oldName, newName)
    move(entry, destination)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        directories = scandir(download_dir)
        for directory in directories:
            name = directory.name
            destination = download_dir
            for image_extension in image_extensions:
                if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                    destination = images_dir
                    move_file(destination, directory, name)

            for video_extension in video_extensions:
                if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                    destination = videos_dir
                    move_file(destination, directory, name)

            for audio_extension in audio_extensions:
                if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                    destination = music_dir
                    move_file(destination, directory, name)

            for document_extension in document_extensions:
                if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                    destination = doc_dir
                    move_file(destination, directory, name)

            if name.endswith(".exe") or name.endswith(".EXE"):
                destination = prog_dir
                move_file(destination, directory, name)

            for compressed_extension in compressed_extensions:
                if name.endswith(compressed_extension) or name.endswith(compressed_extension.upper()):
                    destination = comp_dir
                    move_file(destination, directory, name)

            if name.endswith("torrent") or name.endswith(".TORRENT"):
                destination = torr_dir
                move_file(destination, directory, name)


if __name__ == "__main__":
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Set format for displaying path
    path = download_dir

    # Initialize logging event handler
    event_handler = MoveHandler()

    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
