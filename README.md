# Реализация TensorFlow Object Detection API для Hydronautics team
## Требования
В данном туториале используется Docker. Обучение проводится на GPU. Используется TensorFlow 1, т.к. Object Detection API все еще не не поддерживает TensorFlow 2. CUDA и Cudnn желательно ставить версии 10.0 до обновления OD API.

*Список необходимого:*
- Обновить Nvidia driver
- Установить [CUDA 10.0](https://developer.nvidia.com/cuda-10.0-download-archive) и [Cudnn](https://developer.nvidia.com/rdp/cudnn-archive)
- Установить [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- Установить [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) для поддержки Docker-ом GPU
## Подготовка своего датасета
[Как подготовить датасет к обучению / How to prepare dataset for training](https://github.com/vladushked/dnn_gate_detector/wiki/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D1%82%D0%B0%D1%81%D0%B5%D1%82-%D0%BA-%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8E---How-to-prepare-dataset-for-training)

## Обучение 

`docker run -it --name trainer --mount type=bind,source=/home/vladushked/object_detection_docker,target=/tensorflow/models/research/object_detection/user_folder -p 5000:8888 -p 5001:6006 hydronautics/tensorflow_object_detection`

## Полезные ссылки

Хороший туториал - [How To Train an Object Detection Classifier for Multiple Objects Using TensorFlow (GPU) on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
Официальный репозиторий - [Tensorflow Object Detection API Installation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
[Exporting a trained model for inference](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/exporting_models.md)
