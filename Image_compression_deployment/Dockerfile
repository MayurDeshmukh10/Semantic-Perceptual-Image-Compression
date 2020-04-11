FROM openwhisk/python3aiaction

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        python3-pip \
        gcc \
        libc-dev \
        libxslt-dev \
        libxml2-dev \
        libffi-dev \
        libssl-dev \
        libasound-dev \
        portaudio19-dev \
        python3-pyaudio \
        ffmpeg \
        zip \
        unzip \
        libsm6 \
        libxrender1 \
        libfontconfig1 \
        vim \
        && rm -rf /var/lib/apt/lists/*





RUN pip3 install --upgrade pip


RUN pip3 install \
    numpy==1.15.4 \
    Keras-Applications==1.0.8 \
    Keras-Preprocessing==1.1.0 \
    setuptools>=41.0.0 \
    grpcio>=1.24.3 \
    scipy \
    scikit-image \
    opencv-python \ 
    imageio \ 
    sklearn \
    tensorflow==2.0 \
    keras==2.3.1 \
    numba \
    Pillow \
    piexif \
    pprintpp


RUN apt-get upgrade


ADD model.py /pythonAction
ADD params.py /pythonAction
ADD compression.py /pythonAction
ADD util.py /pythonAction
ADD checkpoint /pythonAction
ADD model-50 /pythonAction
ADD model-50.meta /pythonAction



