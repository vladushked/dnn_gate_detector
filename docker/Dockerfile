# parent image with gpu support
FROM tensorflow/tensorflow:1.14.0-gpu
# update and upgrade
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git python-pip nano
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
RUN pip install opencv-python
# cloning /tensorflow/models
RUN mkdir -p /tensorflow/models
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models
# COCO API installation
RUN git clone https://github.com/cocodataset/cocoapi.git
RUN cd cocoapi/PythonAPI
RUN make
RUN cp -r pycocotools tensorflow/models/research/
# compile protobufs
WORKDIR /tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
# install
RUN python setup.py build
RUN python setup.py install
# export environment variable
RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
WORKDIR /tensorflow/models/research/object_detection/
RUN git clone https://github.com/vladushked/dnn_gate_detector.git
RUN mkdir user_folder

