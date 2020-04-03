# Реализация TensorFlow Object Detection API для Hydronautics team
## Требования
В данном туториале используется Docker. Обучение проводится на GPU. Используется TensorFlow 1, т.к. Object Detection API все еще не не поддерживает TensorFlow 2. CUDA и Cudnn желательно ставить версии 10.0 до обновления OD API.

*Список необходимого:*
- Обновить Nvidia driver
- Установить [CUDA 10.0](https://developer.nvidia.com/cuda-10.0-download-archive) и [Cudnn](https://developer.nvidia.com/rdp/cudnn-archive)
- Установить [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- Установить [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) для поддержки Docker-ом GPU
## Подготовка своего датасета
### Нарезка видео на отдельные кадры
После того, как ты отснял кучу видео с донкой в бассейне тебе нужно сделать из этих видео еще большую кучу картинок. Для этого необходимо использовать скрипт video_to_frames.py (костыльный скрипт, извините), который каждую секунду видео создает изображение.

В командной строке нужно выполнить:  
`python [path_to_your_work_directory]/video_to_frames.py [path_to_your_video] [framerate] [picture_filename] [format]` 
где соответственно:
- [path_to_your_work_directory] - путь к директории в которой лежит скрипт
- [path_to_your_video] - путь к видео
- [framerate] - количество кадров в секунду. Чтобы с каждой секунды видео получать больше фоток, нужно уменьшить это число
- [picture_filename] - название конечных изображений. После него скрипт сам добавляет нумерацию.
- [format] - формат конечных изображений БЕЗ ТОЧКИ: jpg, png и тд.
### Пример
`python video_to_frames.py ../gate_dataset_new/device_camera_image_raw_2019_10_06_12_58_06.avi 12 hydro jpg`
# Размечаем полученные фотографии донного оборудования
Прежде чем перейти к разметке, нужно оставить только те, которые содержат необходимые нам объекты (в принципе логично даааа)
Далее запасаемся чайком и с помощью программы [labelImg](https://github.com/tzutalin/labelImg) отмечаем необходимые объекты
### Объекты
- gate - ворота (у ворот не надо отмечать штанги)
- red_flare - красный столб перед воротами
- yellow_flare - желтый столбик (находится в случайном месте в бассейне)
- mat - полотно с тазиками
- red_bowl - красный тазик
- blue_bowl - синий тазик
## Сборка образа и первый запуск контейнера
```
cd docker
docker build -t hydronautics/tensorflow-gpu-object-detection .
```
*...*
*Можно попить чаЁк*

После сборки образа создаем контейнер и доустанавливаем **python-tk**, т.к. при установке нужно указать регион (при сборке с этим пакетом, тормозится именно на месте, где надо указать регион).
Первая команда запускает контейнер в интерактивном режиме, монтирует Вашу директорию к *user_folder* в контейнере, пробрасывает порты под tensorboard (6006) и сам контейнер (8888. К нему можно подключиться потом по ssh. Подробнее [здесь](https://leimao.github.io/blog/TensorBoard-On-Docker/)). 
```
docker run --gpus all \
    -it --name trainer \
    --mount type=bind,source=[path_to_your_dir],target=/tensorflow/models/research/object_detection/user_folder \
    -p 5000:8888 \
    -p 5001:6006 \
    hydronautics/tensorflow-gpu-object-detection
apt install python-tk
```
## Обучение 
### Структура директории *user_folder*
```
+data
    -label_map.pbtxt (label map file)
    -train.record (train TFRecord file)
    -eval.record (test TFRecord file)
+images
    +eval
        -heap of your test images
        -
        -
    +train
        -heap of your train images
        -
        -
+model
    -fine tuned checkpoint of trained model
+training (here will be your trained model)
    -pipeline config file
```
В директорию **data** нужно поместить `label_map.pbtxt` и отредактировать его под свои объекты.
Далее свои изображения поместить в **images**
В **model** помещаете скачанную с официального [репозитория](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) сетку. 
В директорию **training** поместить config своей сети, взятый из папки [configs](https://github.com/vladushked/dnn_gate_detector/tree/master/configs) моего репозитория или [отсюда](https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs), но тогда пропишите такие же пути к *fine_tuned_checkpoint*, *labels_map*, *train.record* и *eval.record*.
```
cd dnn_gate_detector
git pull
./start_training
```

Если вышли из контейнера, то посмотреть, запущен ли он, можно командой `docker ps` и войти `docker attach trainer`
Если ничего нет, то:
```
docker start trainer
docker attach trainer
```

## Полезные ссылки

Хороший туториал - [How To Train an Object Detection Classifier for Multiple Objects Using TensorFlow (GPU) on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
Официальный репозиторий - [Tensorflow Object Detection API Installation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
[Exporting a trained model for inference](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/exporting_models.md)
