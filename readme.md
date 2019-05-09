[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/datasci4health/harena-logger/blob/master/LICENSE)
[![Docker Automated](https://img.shields.io/docker/cloud/automated/datasci4health/harena-logger.svg?style=flat)](https://cloud.docker.com/u/datasci4health/repository/registry-1.docker.io/datasci4health/harena-logger)
[![Docker Build](https://img.shields.io/docker/cloud/build/datasci4health/harena-logger.svg?style=flat)](https://cloud.docker.com/u/datasci4health/repository/registry-1.docker.io/datasci4health/harena-logger)
[![Docker Pulls](https://img.shields.io/docker/pulls/datasci4health/harena-logger.svg?style=flat)](https://cloud.docker.com/u/datasci4health/repository/registry-1.docker.io/datasci4health/harena-logger)
[![Docker Stars](https://img.shields.io/docker/stars/datasci4health/harena-logger.svg?style=flat)](https://cloud.docker.com/u/datasci4health/repository/registry-1.docker.io/datasci4health/harena-logger)

# harena-logger

[Harena](https://github.com/datasci4health/harena)'s API for managing users and clinical cases.

## Table of Contents 

   * [herena-logger](#herena-logger)
      * [Table of Contents](#table-of-contents)
      * [Getting Started](#getting-started)
         * [Running as Docker containers - Linux](#running-as-docker-containers---linux)
         * [Running as Docker containers - Windows](#running-as-docker-containers---windows)
         * [Running locally - Linux](#running-locally---linux)
         * [Running locally - Windows](#running-locally---windows)
      * [System Requirements](#system-requirements)
         * [For running as Docker containers](#for-running-as-linuxwindows-docker-containers)
         * [For running locally](#for-running-locally)
      * [Configuration](#configuration)
         * [Virtualenvs: AdonisJS](#virtualenvs-adonisjs)
         * [Virtualenvs: Database](#virtualenvs-database)
      * [Contributing](#contributing)
         * [Project organization](#project-organization)
         * [Branch organization (future CI/CD)](#branch-organization-future-cicd)

## Getting Started

### Running as Docker containers - Linux

```bash
sudo apt-get install -y wget
wget https://github.com/datasci4health/harena-manager/blob/master/docker-compose.yml
sudo docker-compose up
```

<small> Make sure you have **node.js** and **npm** already installed (see [system requirements](#system-requirements) for more details). </small>


### Running as Docker containers - Windows

//to do

### Running as Docker containers - Linux´
```bash
sudo docker run datasci4health/harena-logger:latest
```

### Running locally - Linux

First, clone this repository and enter the folder:

```bash
git clone https://github.com/datasci4health/harena-logger 
cd harena-logger
```
```bash
cd modules/relayer                     # entering the source folder
pip3 install -r requirements.txt       # installing requirements packages for python
export FLASK_APP=server.py             # defining flask application
flask run                              # running the application
``` 

### Running locally - Windows

//to do

## System Requirements

### For running as Docker containers

* [docker]()
* [docker-compose]()

### For running locally

##### System dependencies

* flask
* flask-restful
* flask-cors
* paho-mqtt
* pymongo

## Configuration

### Virtualenvs

* HARENA_LOGGER_BROKER_HOST = mqtt host
* HARENA_LOGGER_BROKER_PORT = mqtt host port

* HARENA_LOGGER_FLASK_HOST  = Flask host
* HARENA_LOGGER_FLASK_PORT  = Flask port
* HARENA_LOGGER_FLASK_DEBUG = Flask debug

* HARENA_LOGGER_MONGODB_HOST = mongo host
* HARENA_LOGGER_MONGODB_PORT = mongo port
* HARENA_LOGGER_MONGODB_DB  = mongo database name
* HARENA_LOGGER_MONGODB_COLLECTION = mongo current document

## Contributing

### Project organization

//to do

### Branch organization (future CI/CD)
* **feature/< label >:**
    * new features.
* **development:**
    * Protected. Must use _pull request_ to merge new features.
* **master:**
    * Version running at http://cloud.lis.ic.unicamp.br/harena/latest .
    * Protected. Must use _pull request_ to merge evolutions of the _development_ branch.
* **tags:**
    * Are used for creating Dockerhub image versions at https://cloud.docker.com/u/datasci4health/repository/docker/datasci4health/harena-logger .    
