import json
from pprint import pprint

import numpy as np

from os import path
from vosk import Model, KaldiRecognizer, SpkModel
from src.transcriber.audio_file_tools import (
    get_audio_file_convertor,
    get_audio_file_parser)
from src.transcriber.spk_tools.clusters import get_central_vectors
from src.transcriber.spk_tools.utils import set_speaker


AUDIO_FRAMERATE = 16000
AUDIO_FRAME = 4000
SMALL_MODEL_PATH = 'models/vosk_model/vosk-model-small-ru-0.22'
LARGE_MODEL_PATH = 'models/vosk_model/vosk-model-ru-0.42'
SPEAKER_MODEL_PATH = 'models/vosk_model/vosk-model-spk-0.4'
OUTPUT_PATH = 'tests/fixtures/transcripts/'


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
        return SMALL_MODEL_PATH
    elif model_size == 'large':
        return LARGE_MODEL_PATH


def get_recognizer(model_size):
    model_path = get_model_path(model_size)
    model = Model(model_path)
    speaker_model = SpkModel(SPEAKER_MODEL_PATH)
    recognizer = KaldiRecognizer(model, AUDIO_FRAMERATE)
    recognizer.SetSpkModel(speaker_model)
    return recognizer


def get_dict_res_list(audio_file, recognizer):
    dict_res_list = []

    while True:
        data = audio_file.readframes(AUDIO_FRAME)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            # convert the recognizerResult json string into a dictionary
            result = json.loads(recognizer.Result())
            # save the 'text' value from the dictionary into a list
            # dict_res_list.append(result.fromkeys(['spk', 'text'], None))
            dict_res_list.append({
                'spk': result.get('spk'),
                'text': result.get('text')
            })

    # process "final" result
    result = json.loads(recognizer.FinalResult())
    # dict_res_list.append(result.fromkeys(['spk', 'text'], None))
    dict_res_list.append({
        'spk': result.get('spk'),
        'text': result.get('text')
    })
    return [item for item in dict_res_list if item['text']]


def transcribe(file_path, model_size, num_speakers):
    audio_file = get_audio_file(file_path)
    recognizer = get_recognizer(model_size)
    dict_res_list = get_dict_res_list(audio_file, recognizer)
    # print(f'!!!Dict res list {dict_res_list}')
    speaker_vectors = [item['spk'] for item in dict_res_list if item['spk']]
    # print(f'!!!Speaker vectors {speaker_vectors}')
    central_vectors = get_central_vectors(speaker_vectors, num_speakers)
    # print(f'!!!Central vectors {central_vectors}')
    mapped_list = [set_speaker(item, central_vectors) for item in dict_res_list]

    output_txt = ""
    for item in mapped_list:
        speaker = item['spk']
        text = item['text']
        output_txt += f"\n[{speaker}]: " + text + "\n"

    # write text portion of results to a file
    with open(f"{file_path[:-4]}-{model_size}.txt", 'w', encoding="utf8") as file:
        file.write(output_txt)

    return output_txt


def transcribe2(file_path, model_size='small'):
    audio_file = get_audio_file(file_path)
    # data = audio_file.readframes(audio_file.getnframes())

    model_path = get_model_path(model_size)
    print(f'!!!Model path {model_path} !!!')
    model = Model(model_path)
    speaker_model = SpkModel(SPEAKER_MODEL_PATH)
    rec = KaldiRecognizer(model, audio_file.getframerate())
    rec.SetSpkModel(speaker_model)

    def cosine_dist(x, y):
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    while True:
        data = audio_file.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print("Text:", res["text"])
            if "spk" in res:
                print("X-vector:", res["spk"])
                print("Speaker distance:", cosine_dist(spk_sig, res["spk"]),
                      "based on", res["spk_frames"], "frames")

    print("Note that second distance is not very reliable because utterance is too short. "
          "Utterances longer than 4 seconds give better xvector")

    res = json.loads(rec.FinalResult())
    print("Text:", res["text"])
    if "spk" in res:
        print("X-vector:", res["spk"])
        print("Speaker distance:", cosine_dist(spk_sig, res["spk"]),
              "based on", res["spk_frames"], "frames")


def transcribe3(file_path, model_size='small'):
    audio_file = get_audio_file(file_path)
    # data = audio_file.readframes(audio_file.getnframes())

    model_path = get_model_path(model_size)
    model = Model(model_path)
    speaker_model = SpkModel(SPEAKER_MODEL_PATH)

    rec = KaldiRecognizer(model, audio_file.getframerate())
    rec.SetSpkModel(speaker_model)

    dict_res_list = []

    while True:
        print("!!!N frames:", audio_file.getnframes())
        data = audio_file.readframes(audio_file.getnframes())
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            rec_result = rec.Result()
            # convert the recognizerResult string into a dictionary
            result_dict = json.loads(rec_result)
            # save the 'text' value from the dictionary into a list
            dict_res_list.append(result_dict.fromkeys(['spk', 'text'], None))

            # process "final" result
    result_dict = json.loads(rec.FinalResult())
    pprint(result_dict)
    dict_res_list.append(result_dict.fromkeys(['spk', 'text'], None))
    pprint(dict_res_list)
