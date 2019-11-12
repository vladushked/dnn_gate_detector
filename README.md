# dnn_gate_detector

Исходный туториал можете почитать здесь - [How To Train an Object Detection Classifier for Multiple Objects Using TensorFlow (GPU) on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)

[Tensorflow Object Detection API Installation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)

[Exporting a trained model for inference](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/exporting_models.md)

[Как подготовить датасет к обучению / How to prepare dataset for training](https://github.com/vladushked/dnn_gate_detector/wiki/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D1%82%D0%B0%D1%81%D0%B5%D1%82-%D0%BA-%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8E---How-to-prepare-dataset-for-training)

`docker run -it --rm --name tf -v ~/mywork:/notebooks -p 8888:8888 -p 6006:6006 tensorflow/tensorflow:latest-gpu-py3-jupyter`

`docker run -it --rm -v ~/mywork:/tf -p 8888:8888 -p 6006:6006 tensorflow/tensorflow:1.14.0-py3`

`docker run --gpus all -it --rm -v ~/mywork:/tf -p 8888:8888 -p 6006:6006 tensorflow/tensorflow:1.14.0-py3`

`export PYTHONPATH=$PYTHONPATH:/tf/models/research/:/tf/models/research/slim`

`export PATH=$PATH:~/.local/bin`

`jupyter notebook --ip=0.0.0.0 --allow-root`

`pip install --ignore-installed --upgrade tensorflow-gpu==1.14` — Release with GPU support (Ubuntu and Windows)
