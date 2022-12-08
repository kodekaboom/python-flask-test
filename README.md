# Chuck Norris jokes app

Flask app to get an amount of jokes of chuck norris

## Installation

Make sure that you have [Docker](https://docs.docker.com/engine/install/) installed.

Run.
```bash
docker build -t python-flask-test . 
```

After creating the container.
```bash
docker container run -d -p 3000:3000 python-flask-test:latest
```


## Usage

To get the jokes you only need to make a request to http://localhost:3000/get-jokes
