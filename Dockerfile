# EIDA Routing Service on Docker
# ==============================
# Four files to be copy: 
# routing.cfg; routing.wsgi; default-site.conf; generate_eida_routing_xml_ingv.py
# 
# Build:
# docker build -t "routing:1.1.2" .
# 
# Run:
# docker run -d --name routing-service -p 80:80 routing:1.1.2
#
# Update: just re-build this image (get Routing latest-version from git) 


FROM ubuntu:18.04
MAINTAINER massimo.fares@ingv.it

RUN apt-get update

# install utils
RUN apt-get install -y vim git wget curl iputils-ping

#install Py3
RUN apt update
RUN apt -y install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -y install python3.6

# install Apache
RUN apt-get -y install apache2
COPY routingconf/default-site.conf /etc/apache2/sites-available/000-default.conf

# install Routing
RUN mkdir -p /var/www/eidaws/routing

# cloning version 1
WORKDIR /var/www/eidaws/routing
RUN git clone https://github.com/EIDA/routing.git 1

# copy conf
COPY routingconf/routing.cfg /var/www/eidaws/routing/1/routing.cfg
COPY routingconf/routing.wsgi /var/www/eidaws/routing/1/routing.wsgi
RUN chmod +xr /var/www/eidaws/routing/1/routing.cfg
RUN chmod +xr /var/www/eidaws/routing/1/routing.wsgi

#load apache wsgi module
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN a2enmod wsgi
RUN service apache2 restart

# copy routing.xml
WORKDIR /var/www/eidaws/routing/1/data
COPY routingconf/routing.xml  /var/www/eidaws/routing/1/data/
RUN chmod +xr /var/www/eidaws/routing/1/data/routing.xml

# entryPoint
# COPY docker-entrypoint.sh /usr/local/bin/
# RUN chmod +xr /usr/local/bin/docker-entrypoint.sh
# RUN ln -s usr/local/bin/docker-entrypoint.sh /

# ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 80

# GO!
CMD /usr/sbin/apache2ctl -D FOREGROUND
