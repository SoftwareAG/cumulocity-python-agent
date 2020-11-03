FROM python:3.9
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["run.py"]
