# parent image with gpu support
FROM tensorflow/tensorflow:1.14.0-gpu
# update and upgrade
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git python-pip
RUN pip install --upgrade pip
# installing all dependencies for Object detection API
RUN apt-get install -y protobuf-compiler python-pil python-lxml
RUN pip install Cython
RUN pip install contextlib2
RUN pip install pillow
RUN pip install lxml
RUN pip install jupyter
RUN pip install matplotlib
RUN pip install pandas
# cloning /tensorflow/models
RUN mkdir -p /tensorflow/models
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models
WORKDIR /tensorflow/models/research
# compile protobufs
RUN protoc object_detection/protos/*.proto --python_out=.
# install
RUN python setup.py build
RUN python setup.py install
# export environment variable
RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

RUN git clone https://github.com/vladushked/dnn_gate_detector.git /tensorflow/models/research/object_detection/
WORKDIR /tensorflow/models/research/object_detection/
