FROM ubuntu:18.04

RUN apt update && apt install -y python3 python3-pip gunicorn3 --no-install-recommends
RUN mkdir openkyc && cd openkyc

COPY requirements.txt /openkyc/
RUN pip3 install setuptools
RUN pip3 install --no-cache-dir -r /openkyc/requirements.txt
COPY . /openkyc/
WORKDIR /openkyc

CMD ["gunicorn3","-w 1","-b 0.0.0.0:5005","kyc:app"]