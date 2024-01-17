import io
import wave
from pydub import AudioSegment

# Установка требуемых параметров для WAV формата
DESIRED_SAMPLE_WIDTH = 2
DESIRED_CHANNELS = 1
DESIRED_FRAME_RATE = 16000


def wav_convertor(wav_file):
    sample_width = wav_file.getsampwidth()
    channels = wav_file.getnchannels()
    frame_rate = wav_file.getframerate()
    wav_file.getframerate()
    if (sample_width, channels, frame_rate) == (
            DESIRED_SAMPLE_WIDTH, DESIRED_CHANNELS, DESIRED_FRAME_RATE):
        print('!!!File is already in the desired format')
        return wav_file

    print('!!!Converting wav_file to the desired format')
    print(f'!!!Sample width: {sample_width},'
          f' channels: {channels},'
          f' frame rate: {frame_rate}')
    audio = wave.open(io.BytesIO(), 'wb')
    audio.setframerate(16000)
    audio.setsampwidth(2)
    audio.setnchannels(1)

    # Копируем данные из оригинального файла в новый
    audio.writeframes(wav_file.readframes(wav_file.getnframes()))
    print(f'!!!Converted:'
          f' Sample width: {audio.getsampwidth()},'
          f' channels: {audio.getnchannels()},'
          f' frame rate: {audio.getframerate()}')
    return audio


def mp3_to_wav_converter(mp3_file):
    # Чтение MP3 файла
    audio = AudioSegment.from_mp3(io.BytesIO(mp3_file.read()))

    # Приведение к нужным параметрам
    audio = (audio
             .set_frame_rate(DESIRED_FRAME_RATE)
             .set_sample_width(DESIRED_SAMPLE_WIDTH)
             .set_channels(DESIRED_CHANNELS))

    # Преобразование в массив байт (bytes)
    converted_wav = audio.raw_data
    sample_width = audio.sample_width

    # Создание нового объекта wave с нужными параметрами
    new_wav = wave.open(io.BytesIO(converted_wav), 'wb')
    new_wav.setnchannels(DESIRED_CHANNELS)
    new_wav.setsampwidth(sample_width)
    new_wav.setframerate(DESIRED_FRAME_RATE)
    new_wav.setnframes(
        len(converted_wav) // (sample_width * new_wav.getnchannels()))
    return new_wav


def get_audio_file_convertor(file_extension):
    match file_extension:
        case '.wav':
            return lambda audio_file: wav_convertor(audio_file)
        case '.mp3':
            return lambda audio_file: mp3_to_wav_converter(audio_file)
        case _:
            raise ValueError('File format is not supported by converter')
