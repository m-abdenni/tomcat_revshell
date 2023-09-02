#!/bin/bash

# update packages
sudo apt update -y

# install java
sudo apt-get install -y default-jdk

# create tomcat user and group
sudo groupadd tomcat
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat

# extract tomcat files
# sudo mkdir -p /opt/tomcat
cd /opt/
sudo tar -xzvf /vagrant/tomcat-8.5.5.tar.gz

# config permissions
# cd /opt/tomcat
# sudo chgrp -R tomcat /opt/tomcat
# sudo chmod -R g+r conf
# sudo chmod g+x conf
# sudo chown -R tomcat webapps/ work/ temp/ logs/

# look for java location to add it to the path
sudo update-java-alternatives -l
export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
export CATALINA_HOME=/opt/tomcat

# Copy tomcat.service to /etc/systemd/system
sudo cp /vagrant/tomcat.service /etc/systemd/system/

# reload system deamon
sudo systemctl daemon-reload

# start tomcat & and confim it is working
sudo systemctl start tomcat
sudo systemctl status tomcat

# Cleaning
# delete the user and the group
sudo deluser vagrant
sudo delgroup vagrant

# delete the home directory
sudo rm -rf /home/vagrant
sudo umount /vagrant