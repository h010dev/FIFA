#
# Dockerfile for scrapyd:py3
#

# Use python:3.7.3-strech instead of debian:stretch to use pip3
FROM python:3.7.3-stretch
MAINTAINER kev <noreply@easypi.pro>

# Custom workdir to copy requirements to for pip install
WORKDIR /app
COPY ./requirements.txt /app

RUN set -xe \
    && apt-get update \
    && apt-get install -y autoconf \
                          build-essential \
                          curl \
                          git \
                          libffi-dev \
                          libssl-dev \
                          libtool \
                          libxml2 \
                          libxml2-dev \
                          libxslt1.1 \
                          libxslt1-dev \
                          python \
                          python-dev \
                          vim-tiny \
    && apt-get install -y libtiff5 \
                          libtiff5-dev \
                          libfreetype6-dev \
                          libjpeg62-turbo \
                          libjpeg62-turbo-dev \
                          liblcms2-2 \
                          liblcms2-dev \
                          libwebp6 \
                          libwebp-dev \
                          zlib1g \
                          zlib1g-dev \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python \
    && pip install git+https://github.com/scrapy/scrapy.git \
                   git+https://github.com/scrapy/scrapyd.git \
                   git+https://github.com/scrapy/scrapyd-client.git \
                   git+https://github.com/scrapinghub/scrapy-splash.git \
                   git+https://github.com/scrapinghub/scrapyrt.git \
                   git+https://github.com/python-pillow/Pillow.git \
    && curl -sSL https://github.com/scrapy/scrapy/raw/master/extras/scrapy_bash_completion -o /etc/bash_completion.d/scrapy_bash_completion \
    && echo 'source /etc/bash_completion.d/scrapy_bash_completion' >> /root/.bashrc \
    && echo 'installing user-defined packages' \
    && echo 'installing Cython and line_profiler' \
    && apt-get update && apt-get install -y gcc \
    && pip install Cython \
    && mkdir ~/line_profiler \
    && cd ~/line_profiler && git clone https://github.com/rkern/line_profiler.git \
    && find line_profiler -name '*.pyx' -exec cython {} \; && cd line_profiler \
    && pip install . --user \
    && echo 'installing RedisJSON' \
    && pip install rejson \
    && mkdir ~/rejson \
    && cd ~/rejson && git clone https://github.com/RedisJSON/RedisJSON.git && cd RedisJSON && make \
    && echo 'installing other pip packages' \
    && pip install -r /app/requirements.txt \ 
    && apt-get purge -y --auto-remove autoconf \
                                      build-essential \
                                      libffi-dev \
                                      libssl-dev \
                                      libtool \
                                      libxml2-dev \
                                      libxslt1-dev \
                                      python-dev \
    && apt-get purge -y --auto-remove libtiff5-dev \
                                      libfreetype6-dev \
                                      libjpeg62-turbo-dev \
                                      liblcms2-dev \
                                      libwebp-dev \
                                      zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./scrapyd.conf /etc/scrapyd/
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
EXPOSE 6800

CMD ["scrapyd", "--pidfile="]
