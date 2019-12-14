FROM python:3

RUN mkdir /usr/local/lib/neterraproxy && \
    pip install --upgrade pip && \
    pip install neterraproxy

ENTRYPOINT python -m neterraproxy $USER $PASSWORD $DATADIR

 
