FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY dist/jgtagentic-*.whl /tmp/
COPY requirements.txt requirements-test.txt ./

RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install -r requirements-test.txt

RUN pip install /tmp/jgtagentic-*.whl

COPY . .

ENTRYPOINT ["/bin/bash"]
CMD ["run_agentic_tests.sh"] 