FROM python:3.5

MAINTAINER Joshy Cyriac <j.cyriac@gmail.com>

# Install uWSGI
RUN pip install uwsgi

# Standard set up Nginx
ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
    && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
    && rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443 8888
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*

# Clone latest from master
RUN git clone  https://github.com/joshy/meta.git
WORKDIR /meta
RUN pip install -r requirements.txt
RUN pip install -r requirements-notebooks.txt
RUN mkdir instance
COPY scripts/config.cfg /meta/instance

# Copy the modified Nginx conf
COPY scripts/nginx.conf /etc/nginx/conf.d/

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY scripts/uwsgi.ini /etc/uwsgi/


# Custom Supervisord config
COPY scripts/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# WORKDIR /meta/notebooks

# Start the supervisor of all applications
CMD ["/usr/bin/supervisord"]
