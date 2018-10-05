# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools
from .python import Python
from .opencv import Opencv


@dependency(Tools, Python, Opencv)
@source('git')
class Caffe2(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        switcher = 'OFF' if self.composer.cuda_ver is None else 'ON'
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libprotobuf-dev \
                protobuf-compiler \
                && \

            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                enum34 \
                pyyaml \
                typing \
                && \

            $GIT_CLONE https://github.com/pytorch/pytorch.git \
                ~/caffe2 --branch master --recursive && \
            cd ~/caffe2 && mkdir build && cd build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D USE_CUDA=%s \
                  -D USE_MPI=OFF \
                  -D USE_NNPACK=OFF \
                  -D USE_ROCKSDB=OFF \
                  -D BUILD_TEST=OFF \
                  .. && \
            make -j"$(nproc)" install && \
        ''' % switcher
