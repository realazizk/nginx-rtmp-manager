#!/usr/bin/env bash

###
# Audio Stream Manager
# Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017
###


###
# Config
###

export DEV=1

###
# Prepare dependencies
###
sudo apt-get update -y
sudo apt-get install git -y
mkdir -p /home/vagrant/.local/bin/
git clone https://github.com/arut/nginx-rtmp-module.git --depth=1
git clone https://github.com/nginx/nginx.git --depth=1


###
# Prepare Nginx
###

sudo apt-get -y install build-essential zlib1g-dev libpcre3-dev libbz2-dev \
     libssl-dev tar unzip

cd nginx
auto/configure --add-module=../nginx-rtmp-module --prefix=/home/vagrant/.local
make
make install

sudo setcap CAP_NET_BIND_SERVICE=+eip /home/vagrant/.local/sbin/nginx
ln -s /home/vagrant/.local/sbin/nginx /home/vagrant/.local/bin/nginx
export PATH=$PATH:~/.local/bin
echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc

###
# Prepare the database
###

sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-9.3  -y
sudo su postgres -c "psql -c \"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant'\" "
export DATABASE_URL="postgresql://vagrant:vagrant@localhost/database"
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O vagrant database"

###
# Application
###

cd /app

cp -r nginx.conf /home/vagrant/.local/conf/nginx.conf

sudo apt-get install pkg-config libavresample-dev libavdevice-dev libavfilter-dev libswscale-dev libyaml-dev libffi-dev -y

curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -

sudo apt-get install npm nodejs -y

sudo npm install npm@latest -g

sudo ln -s /usr/bin/nodejs /usr/bin/node

sudo pip3.6 install -r requirements/dev.txt
