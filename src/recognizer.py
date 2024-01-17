import argparse
# TODO:make import from package
from src.transcriber.transcriber import transcribe


def setup_cli_parser():
    parser = argparse.ArgumentParser(
        description='Recognizes and analyzes speech in audio format in Russian')
    parser.add_argument('file_path')
    parser.add_argument('-m', '--model_size')
    args = parser.parse_args()
    return args


def main():
    args = setup_cli_parser()
    text = transcribe(file_path=args.file_path, model_size=args.model_size)
    print(text)


if __name__ == '__main__':
    main()
