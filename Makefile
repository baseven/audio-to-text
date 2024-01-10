install:
	poetry install

say-hello:
	poetry run say-hello

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 speech_recognition

package-update: lint build publish package-install
