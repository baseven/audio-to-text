install:
	poetry install

recognize:
	poetry run recognize

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 src

package-update: build publish package-install
