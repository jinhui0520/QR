FROM python:3.9-slim
WORKDIR /app
EXPOSE 80
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
