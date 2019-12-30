# FlaskAPOD
A simple flask app to communicate with NASA's APOD API written in Python using Flask
# Installation
 1. Start by cloning the repository by running: `git clone https://github.com/vishalbala-nps/FlaskAPOD`
 2. After cloning the Repository, download required modules by typing `pip3 install -r requirements.txt` You should run this inside the cloned directory 
 3. After installation of dependencies, run the app by running: `gunicorn app:app` This will start the app in your local machine. You can access it by typing: `127.0.0.1:8000` in your browser
 # Deploying on Heroku
 This repo comes with a Heroku Procfile to help you deploy the flask app on Heroku. This app is already hosted on Heroku. You can visit it [here](https://flask-apod.herokuapp.com/)
# Contaierising FlaskAPOD
This repo includes a Dockerfile for running the app on Docker/Podman. A sample asciinema recording is [here](https://asciinema.org/a/291002)
