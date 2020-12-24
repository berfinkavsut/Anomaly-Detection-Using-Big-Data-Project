FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_DEFAULT_TIMEOUT=100
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

## Util packages

RUN apt-get update
RUN pip install pylint==2.4.1
RUN pip install mock==3.0.5
RUN pip install nose==1.3.7
RUN pip install nose-cov==1.6
RUN pip install coverage==4.5.4
RUN pip install Sphinx==3.0.0
RUN pip install sphinxcontrib-napoleon==0.7.0
RUN pip install sphinx-rtd-theme==0.4.3

## Base python packages

RUN pip install numpy==1.9.0
RUN pip install pandas==1.1.5
RUN pip install scipy==1.5.4
RUN pip install scikit-learn==0.24.0
RUN pip install matplotlib==3.3.3
RUN pip install joblib==1.0.0
RUN pip install seaborn==0.11.1
RUN pip install Flask==1.1.2
RUN pip install h5py==3.1.0

WORKDIR /workspace