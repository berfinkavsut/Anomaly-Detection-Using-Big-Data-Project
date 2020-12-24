# network-anomaly-detection

This project contains files for the network anomaly detection framework.

## Setting Up Working Environment

Docker base image setup:

`docker build -t databoss/nad:base docker/base`

After building the base image, run the following command to build the development image:

`docker build -t databoss/nad:development docker/development`

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
