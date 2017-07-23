# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "public_network", bridge: "wlp3s0"
  config.vm.provision :shell, :privileged => true, :path => "installpy.sh"
  config.vm.provision :shell, :privileged => false, :path => "provision.sh"
  config.vm.synced_folder ".", "/app"
  config.vm.network "forwarded_port", guest: 5000, host: 8080
  config.vm.network "forwarded_port", guest: 8080, host: 8090
end
