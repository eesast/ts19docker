# According to a excellent blog of bitJudo
# http://bitjudo.com/blog/2014/03/13/building-efficient-dockerfiles-node-dot-js/
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
#RUN apt-get install python-dev
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ADD . /code/
