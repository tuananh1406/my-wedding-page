# pull official base image
FROM python:3.9.13

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
ADD . /code


# install psycopg2 dependencies
RUN \
    # --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    # --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && \
    apt-get install -y postgresql-contrib gcc python3-dev musl-dev libgl-dev vim

# install dependencies
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --python=3.9
# WORKDIR /code/docker
# RUN sh install.sh

# setup timezone
ENV TZ 'Asia/Ho_Chi_Minh'
RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

EXPOSE 8000
