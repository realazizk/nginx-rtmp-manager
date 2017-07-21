#!/usr/bin/env bash

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
# Application
###

cd /app

cp -r nginx.conf /home/vagrant/.local/conf/nginx.conf

sudo apt-get install python3 python3-pip libyaml-dev -y

curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -

sudo apt-get install npm nodejs -y

sudo npm install npm@latest -g

sudo ln -s /usr/bin/nodejs /usr/bin/node

sudo pip3 install -r requirements/dev.txt
