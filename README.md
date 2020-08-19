# Как обучить нейросеть для детектирования соих объектов на GPU, Tensorflow 2 Object Detection API
# How to train an object detection classifier on custom dataset using TensorFlow 2 Object Detection API and Docker on GPU
*for [Hydronautics team](https://vk.com/hydronautics)*
## Требования

- Обновить Nvidia driver
- Установить [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-base) и [Cudnn](https://developer.nvidia.com/rdp/cudnn-archive)
- Установить [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- Установить [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
## Подготовка своего датасета
### Нарезка видео на отдельные кадры 

В командной строке:  
```bash
python [path_to_your_work_directory]/video_to_frames.py [path_to_your_video] [framerate] [picture_filename] [format]
``` 
где:
- [path_to_your_work_directory] - путь к директории в которой лежит скрипт
- [path_to_your_video] - путь к видео
- [framerate] - количество кадров в секунду. Чтобы с каждой секунды видео получать больше фоток, нужно уменьшить это число
- [picture_filename] - название конечных изображений. После него скрипт сам добавляет нумерацию.
- [format] - формат конечных изображений БЕЗ ТОЧКИ: jpg, png и тд.
**Пример**
```bash
python video_to_frames.py ../gate_dataset_new/device_camera_image_raw_2019_10_06_12_58_06.avi 12 hydro jpg
```
### Разметка полученных фотографий
С помощью программы [labelImg](https://github.com/tzutalin/labelImg) отмечаем необходимые объекты на каждой фотографии
Примеры объектов:
- gate - ворота (у ворот не надо отмечать штанги)
- red_flare - красный столб перед воротами
- yellow_flare - желтый столбик (находится в случайном месте в бассейне)
- mat - полотно с тазиками
- red_bowl - красный тазик
- blue_bowl - синий тазик
### Перемешивание изображений и создание выборок
Далее необходимо перемешать все изображения скриптом **randomData.py** (--help есть). Этот скрипт формирует папочку *data* с подпапками *train* и *eval*. По умолчанию скрипт отбирает случайно 20% изображений для тестовой выборки. Required только -i/--images путь до папки с изображениями. Если размечали вы в программе labelImg, то .xml метки у вас будут в той же директории, что и изображения.
**Пример**
```bash
python randomData.py -i /home/vladushked/hydro/images/
python randomData.py -i /home/vladushked/hydro/images/ -l /home/vladushked/hydro/labels/ -p 0.15
```
### Подготовка датаcета для обучения
С помощью скрипта `xml_to_csv.py` формируем 2 файла train_labels.csv и eval_labels.csv
Далее в скрипте `generate_tfrecord.py` надо добавить свои метки 
```
# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'gate':
        return 1
    elif row_label == 'red_flare':
        return 2
    elif row_label == 'yellow_flare':
        return 3
    elif row_label == 'red_bowl':
        return 4
    elif row_label == 'blue_bowl':
        return 5
    else:
        return None
```
и с помощью него создаем 2 файла TFrecord. 

```bash
python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record
python generate_tfrecord.py --csv_input=images/eval_labels.csv --image_dir=images/eval --output_path=eval.record
```
## Создание label map

В директории data создаем файл со своими метками
```
item {
  id: 1
  name: 'gate'
}

item {
  id: 2
  name: 'red_flare'
}

item {
  id: 3
  name: 'yellow_flare'
}

item {
  id: 4
  name: 'red_bowl'
}

item {
  id: 5
  name: 'blue_bowl'
}

```
##

Далее из директории [configs/tf2 folder](https://github.com/tensorflow/models/tree/master/research/object_detection/configs/tf2) копируем в папку training наш конфиг

* Line 13: change the number of classes to number of objects you want to detect (4 in my case)

* Line 141: change fine_tune_checkpoint to the path of the model.ckpt file:

    * ```fine_tune_checkpoint: "<path>/efficientdet_d0_coco17_tpu-32/checkpoint/ckpt-0"```

* Line 143: Change ```fine_tune_checkpoint_type``` to detection

* Line 182: change input_path to the path of the train.records file:

    * ```input_path: "<path>/train.record"```

* Line 197: change input_path to the path of the test.records file:

    * ```input_path: "<path>/test.record"```

* Line 180 and 193: change label_map_path to the path of the label map:

    * ```label_map_path: "<path>/labelmap.pbtxt"```

* Line 144 and 189: change batch_size to a number appropriate for your hardware, like 4, 8, or 16.


## Сборка образа 

Склоньте репозиторий [Object Detection API](https://github.com/tensorflow/models.git)
Далее 

```bash
cd models
docker build -f research/object_detection/dockerfiles/tf2/Dockerfile -t od .
```
*...*
*Можно попить чаёк*

## Создание контейнера
Первая команда запускает контейнер в интерактивном режиме, монтирует Вашу директорию к *user_folder* в контейнере, пробрасывает порт под tensorboard
```bash
docker run --gpus all \
    -it --name trainer \
    --mount type=bind,source=[path_to_your_dir],target=/home/tensorflow/models/research/object_detection/user_folder \
    -p 6006:6006 \
    od
```
## Запуск контейнера
```bash
docker start trainer
docker attach trainer
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
1. В директорию **data** нужно поместить `label_map.pbtxt` и отредактировать его под свои объекты.
2. Далее свои изображения поместить в **images**.
3. В **model** помещаете скачанную с официального [репозитория](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) сеть
4. В директорию **training** поместить config своей сети.
```bash
python model_main_tf2.py --pipeline_config_path=path_to_config --model_dir=path_to_training_dir --alsologtostderr
```
Если вышли из контейнера, то посмотреть, запущен ли он, можно командой `docker ps` и войти `docker attach trainer`
Если ничего нет, то:

## Запуск Jupyter Notebook

```bash
pip3 install jupyter
```
Из директории object_detection 
```bash
jupyter notebook --ip 0.0.0.0 --port 9999 --no-browser

```
## Полезные ссылки

[How to train a custom object detection model with the Tensorflow 2 Object Detection API](https://github.com/TannerGilbert/Tensorflow-Object-Detection-API-Train-Model)
Хороший туториал - [How To Train an Object Detection Classifier for Multiple Objects Using TensorFlow (GPU) on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
Официальный репозиторий - [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)
На хабре на русском - [Инструкция по работе с TensorFlow Object Detection API](https://habr.com/ru/company/nix/blog/422353/)
На Medium - [TensorFlow Object Detection with Docker from scratch](https://towardsdatascience.com/tensorflow-object-detection-with-docker-from-scratch-5e015b639b0b)
