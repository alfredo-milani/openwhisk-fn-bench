FROM openwhisk/python3action:latest

RUN apk add --update py-pip

# needed for Pillow
RUN apk add jpeg-dev zlib-dev

RUN pip install -v certifi==2020.12.5
RUN pip install -v chardet==4.0.0
RUN pip install -v idna==2.10
RUN pip install -v Pillow==8.2.0
RUN pip install -v redis==3.5.3
RUN pip install -v requests==2.25.1
RUN pip install -v urllib3==1.26.4
