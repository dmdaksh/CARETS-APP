# CARETS APP
<!-- Put an image -->
![CARETS-APP](thumbnail.png)


## CA-ncer

## RE-lated

## T-erms

## S-earch

<!-- make horizontal line -->
<hr>

<!-- Table of content  -->
## Table of Contents
- [Introduction](#introduction)
- [Usage](#usage)
- [Python Requirements](#python-requirements)
- [Data Structure](#data-structure)


## Introduction

### One stop search application for cancer and related terms.

The impetus behind this search application is to provide one stop search for cancer and related terms. User can search for cancer and related terms and get results about the clinical trials and case studies. The application is built using Flask and Next.js.


## Usage

This is a dockerized application. To run the application, you need to have docker installed on your machine. Once, you have docker installed, you can run the application by following steps:

First of all, you need to get SEERS API key and store it in a file called `.env` in the a root directory of the backend. The file should look like this:

``` bash
SEERS_API_KEY=<your_api_key>
```

Then, you need to build the docker images for both the frontend and backend. To do that, run the following commands:

``` bash
docker-compose build
```

Once the images are built, you can run the application by running the following command:

``` bash
docker-compose up
```

The frontend will be running on port 3000 and backend will be running on port 5000. You can access the application on http://localhost:3000 and the backend on http://localhost:5000. The backend is a set of REST APIs which are consumed by the frontend.


## Python Requirements

All of the python requirements are listed in `requirements.txt` file in the backend directory. The dockerfile is running following commands to install the requirements by running the following command. There is no action required from the user.

``` bash
pip install -r requirements.txt
```

These are the list of python libraries other than python inbuilt libraries used in the backend:

- Flask
- Flask-Cors
- Flask-SQLAlchemy
- Python-Dotenv
- Requests

## Data Structure