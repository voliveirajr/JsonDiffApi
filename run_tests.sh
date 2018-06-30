export FLASK_ENV=development
docker pull mongo:3.2.4
docker run -p 27017:27017 --name mongo_test -d mongo:3.2.4 --smallfiles
pytest
docker stop mongo_test
docker rm mongo_test
