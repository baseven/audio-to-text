import wave
from pydub import AudioSegment


def get_audio_file_parser(file_extension):
    match file_extension:
        case '.wav':
            return lambda file_path: wave.open(file_path, "rb")
        case '.mp3':
            return lambda file_path: AudioSegment.from_mp3(file_path)
        case _:
            raise ValueError('File format is not supported by parser')
