FROM python:2.7

EXPOSE 5000

ENV PYTHON_PATH /usr/src/app

WORKDIR /usr/src/app

RUN pip install flask flask_restful pandas

COPY main.py .
COPY query_count_concept_attributes.tsv .

CMD [ "python", "-m", "main" ]
