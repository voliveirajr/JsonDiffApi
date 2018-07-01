# JsonDiffAPI

The purpose is exercise an rest api to receive two json objects encoded in base64 and return their differences.
The problem requested 3 endpoints:

`<host>/v1/diff/<ID>/left`

`<host>/v1/diff/<ID>/right`

To provide documents to be compared

`<host>/v1/diff/<ID>`

To request the result

This application consists in a containerized Flask Rest api running aside a MongoDB container

## Requirements
This application was developed and tested using:
* Python 2.7.13
* Docker 17.12.0-ce
* Docker-compose version 1.18.0
* Virtualenv 15.1.0

## TL;DR
if you know all setup steps just:

run `docker-compose up -d`

Application served at `http://localhost:8080`

## Environment setup
Create a new environment with virtualenv

`virtualenv env`

load it

`source env/bin/activate`

install requirements

`pip install -r requirements.txt`

## Testing
Tests are available running this script
`./run_tests.sh`

## API Usage
To create a new diff object and feed with left and right documents you can curl it passing the json document coded in base64 and using an id of your choice

`curl -X POST -i 'http://127.0.0.1:8080/v1/diff/111111111/left' --data eW91IHNob3VsZCBoaXJlIG1lIHRobw==`

`curl -X POST -i 'http://127.0.0.1:8080/v1/diff/111111111/right' --data eW91IHNob3VsZCBoaXJlIG1lIHRobw==`

To retrieve the result you execute a get by id you defined

`curl -X GET -i 'http://127.0.0.1:8080/v1/diff/111111111'`

:warning: Considering the purpose of the tool, in order to save resources all requests have a TTL of 1 hour, after that they will be automatically removed from database.

## Response examples

The response returned is a json object with a result element or error

error:

`{ "error": "Resource does not exist" }`

valid requests examples"

`{
    "result": "objects have no difference"
}`

when idenfied the differences it returns mentioning what sould be deleted, inserted and/or deleted

`{
  "result": {
    "delete": [
      "test"
    ],
    "insert": {
      "newfield": "lerolero"
    },
    "update": {
      "name": "volmar"
    }
  }
}`

## Improvements
Following a list of possible improvements ordered by priority:
* Database authentication
* HTTP authentication
* Nginx loadbalancing
* Swagger UI
* Ansible or Kubernetes automation

## Author
 Volmar Oliveira Junior
 volmar.oliveira.jr@gmail.com
