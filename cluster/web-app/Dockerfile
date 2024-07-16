FROM python:3.11.9-slim


ENV SRC_DIR /flaskapp

ENV FLASK_APP index
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
ENV FLASK_FORM_SECRET bachmatch_secret

ENV WEAVSERVERHOST bachmatch-weaviate
ENV WEAVSERVERPORT 80
ENV WEAVGRPCSERVERHOST bachmatch-weaviate-grpc
ENV WEAVGRPCSERVERPORT 50051

ENV KAFKABOOTSTRAP bachmatch-kafka-bootstrap:9092

COPY *.py requirements.txt ${SRC_DIR}/
COPY data/*.csv ${SRC_DIR}/data/
COPY templates/* ${SRC_DIR}/templates/



WORKDIR ${SRC_DIR}

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 3030
#CMD ["python","-m", "flask", "run", "-h", "localhost", "-p", "3030"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=3030"]
#CMD ["python", "index.py"]
