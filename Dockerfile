FROM localhost:5000/backend-comm
MAINTAINER Pål Karlsrud <paal@128.no>

ENV BASE_DIR "/var/search"

RUN git clone https://github.com/microserv/search ${BASE_DIR}
RUN apk add --update curl

RUN cp ${BASE_DIR}/search.ini /etc/supervisor.d/
RUN mv ${BASE_DIR}/local_config.py.example ${BASE_DIR}/local_config.py

RUN virtualenv ${BASE_DIR}/venv
ENV PATH ${BASE_DIR}/venv/bin:$PATH

WORKDIR ${BASE_DIR}
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords

RUN rm -rf /run && mkdir -p /run

ENV SERVICE_NAME search

EXPOSE 80
