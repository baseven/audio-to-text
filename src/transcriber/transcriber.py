import json
from os import path
from vosk import Model, KaldiRecognizer
from src.transcriber.audio_file_tools import (
    get_audio_file_convertor,
    get_audio_file_parser)


def get_audio_file(file_path):
    _, file_extension = path.splitext(file_path)
    print(f'!!!Recognizing file_path {file_path} '
          f'with file_extension {file_extension}')
    audio_file_parser = get_audio_file_parser(file_extension)
    audio_file = audio_file_parser(file_path)
    audio_file_convertor = get_audio_file_convertor(file_extension)
    return audio_file_convertor(audio_file)
    # with audio_file_parser(file_path) as audio_file:
    #     audio_file_convertor = get_audio_file_convertor(file_extension)
    #     return audio_file_convertor(audio_file)


def get_model_path(model_size):
    if model_size == 'small':
        return 'models/vosk_model/vosk-model-small-ru-0.22'
    elif model_size == 'large':
        return 'models/vosk_model/vosk-model-ru-0.42'


def transcribe(file_path, model_size='small'):
    audio_file = get_audio_file(file_path)
    data = audio_file.readframes(audio_file.getnframes())
    # print(f'!!!Audio file {data} read')

    model_path = get_model_path(model_size)
    print(f'!!!Model path {model_path} !!!')
    model = Model(model_path)

    offline_recognizer = KaldiRecognizer(model, audio_file.getframerate())
    offline_recognizer.AcceptWaveform(data)
    print(offline_recognizer.Result())
    recognized_data = json.loads(offline_recognizer.Result())["text"]
    return recognized_data
