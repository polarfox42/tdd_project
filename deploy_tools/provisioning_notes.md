Provisioning a new site
=======================

## Required packages

* nginx
* python 3.8
* virtualenv + pip
* Git

eg, on Ubuntu:

	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python3.8 python3.8-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with your site name, eg, yandex.ru
* replace username with the name of user

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, eg, yandex.ru
* replace username with the name of user

## Folder structure
Assume we have a user account at /home/username

/home/username
|-- sites
    |-- SITENAME
	|-- database
	|-- source
	|-- static
	|-- virtualenv        
