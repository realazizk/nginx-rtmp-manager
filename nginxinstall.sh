#!/usr/bin/env bash

[>83;40500;0c
git clone https://github.com/arut/nginx-rtmp-module.git --depth=1
git clone https://github.com/nginx/nginx.git --depth=1

cd nginx
auto/configure --add-module=../nginx-rtmp-module --prefix=/home/mo/.local
make
make install

sudo setcap CAP_NET_BIND_SERVICE=+eip /home/mo/.local/sbin/nginx
ln -fs /home/mo/.local/sbin/nginx /home/mo/.local/bin/nginx
