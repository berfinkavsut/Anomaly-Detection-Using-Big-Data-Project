# Anomaly Detection Using Big Data

## Contributors
* Beste Aydemir 
* Berfin Kavşut
* Şevki Gavrem Kulkuloğlu
* Ege Ozan Özyedek
* Meltem Toprak

This repository contains files for the network anomaly detection framework. The project was undertaken as part of the EEE493/494 Industrial Design Projects I-II courses at Bilkent University during the Fall Semester of 2020 and the Spring Semester of 2021.

My individual contributions to this project included the development of feature extractors within custom modules and collaboration with Şevki Gavrem Kulkuloğu on transformer modules for preprocessing tasks. For the feature extractors, the Tensorflow framework was employed for various extractors, such as the LSTM autoencoder. Additionally, other feature extractors, namely Kitsune and Ip2Vec extractors, were also utilized in this project

## Setting Up Working Environment

Docker base image setup:

`docker build -t databoss/nad:base docker/base`

After building the base image, run the following command to build the development image:

`docker build -t databoss/nad:development docker/development`

You may also need to build the docker image for KAFKA service with the following command:

`docker build -t databoss/nad:kafka wurstmeister/kafka`

## Running the Code From Container

Once the containers are prepared, you can run the following command to start the docker
container that runs the main code as a background process:

`docker run -dit --rm -p 1414:1414 -v $(pwd):/workspace databoss/nad:development python webapp.py`

The request handler will be alive after this command. Later, you can send requests and wait for 
answers.

## Running the Unittests

To run all unittests inside the tests/ directory, run the following command:

`nosetests -vv --exe --with-xunit --with-coverage --cover-xml tests`

## Code Quality Monitoring

To check the code quality inside a script, you can run the following command:

`pylint script_to_be_tested.py`

## Data Sets
[This link](https://drive.google.com/drive/folders/1RZAkaWuvPs1LZunW0LdebhCafABl4pT7?usp=sharing) contains the data sets used in algorithm evaluations along with their explanations. 

