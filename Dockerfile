FROM python:3.6
WORKDIR /app
COPY . .
RUN pip3 install -r /app/requirements.txt
EXPOSE 8080
CMD ["python3",  "/app/app.py"]
