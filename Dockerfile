FROM python:3.9

RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    vim \
    virtualenv \
    wget \
    xpra \
    xserver-xorg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 


RUN virtualenv --python=python3.9 env

RUN ln -s /env/bin/python3.9 /usr/bin/python

RUN curl -o /usr/local/bin/patchelf https://s3-us-west-2.amazonaws.com/openai-sci-artifacts/manual-builds/patchelf_0.9_amd64.elf \
    && chmod +x /usr/local/bin/patchelf

ENV LANG C.UTF-8

RUN pip install --no-cache-dir gym==0.26.2
RUN pip install --no-cache-dir opencv-python==4.6.0.66
RUN pip install --no-cache-dir tqdm==4.64.1
RUN pip install --no-cache-dir PyOpenGL==3.1.7
RUN pip install --no-cache-dir PyOpenGL_accelerate==3.1.7


RUN mkdir /projects; 
RUN git clone https://github.com/glfw/glfw.git /projects/glfw

RUN apt-get update
RUN apt-get install -y zip g++ curl xvfb xorg-dev cmake libzmq3-dev libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev libwayland-dev libxkbcommon-dev

RUN cd /projects/glfw; \
    cmake -DBUILD_SHARED_LIBS=ON .; \
    make;

ENV PYGLFW_LIBRARY=/projects/glfw/src/libglfw.so
ENV MUJOCO_GL=egl
ENV PYOPENGL_PLATFORM=egl

RUN apt-get install -y swig
RUN pip install --no-cache-dir pygame
RUN pip install --no-cache-dir Box2D
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir box2d box2d-kengz