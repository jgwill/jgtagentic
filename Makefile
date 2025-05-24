version := $(shell python3 -c 'from jgtagentic import version; print(version)')
SHELL := /bin/bash

.PHONY: venv
venv:
	[ -d .venv ] || virtualenv .venv --python=jgtagentic
	conda activate jgtagentic

.PHONY: piplocal
piplocal:
	pip install -e '.[dev]'

.PHONY: develop
develop: venv piplocal

.PHONY: lint lint-flake8 lint-isort
lint-flake8:
	flake8 test jgtagentic
lint-isort:
	isort --check-only -rc jgtagentic test *.py
lint: lint-flake8 lint-isort

.PHONY: format
format:
	isort -rc jgtagentic test *.py

.PHONY: test
test:
	coverage run -m py.test
	coverage report

.PHONY: readme_check
readme_check:
	./setup.py check --restructuredtext --strict

.PHONY: clean
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	rm -Rf dist
	rm -Rf *.egg-info

.PHONY: authors
authors:
	git log --format='%aN <%aE>' `git describe --abbrev=0 --tags`..@ | sort | uniq >> AUTHORS
	cat AUTHORS | sort --ignore-case | uniq >> AUTHORS_
	mv AUTHORS_ AUTHORS

.PHONY: bump_jgtpy
bump_jgtpy:
	. /opt/binscripts/load.sh && _bump_jgtpy

.PHONY: dist
dist:
	make clean
	make pre-build
	python -m build

.PHONY: disto
disto:
	make clean
	python setup.py sdist --format=gztar bdist_wheel

.PHONY: pypi-release
pypi-release:
	twine --version
	twine upload dist/*

.PHONY: dev-pypi-release
dev-pypi-release:
	twine --version
	twine upload --repository pypi-dev dist/*

.PHONY: dev-release
dev-release:
	python bump_version.py
	bump:dev &> /dev/null
	make dist
	make dev-pypi-release

.PHONY: dev-release-plus
dev-release-plus:
	make dev-release
	twine upload dist/*

.PHONY: bump_version
bump_version:
	python bump_version.py

.PHONY: release
release:
	make dist
	git tag  $(version)
	git push origin $(version)
	git push
	make pypi-release

.PHONY: pre-build
pre-build:
	#bash pre-build.sh
	#bash pre-dist-fdb_scan.sh||true

.PHONY: quick-release
quick-release:
	make bump_version
	make dist
	make pypi-release
