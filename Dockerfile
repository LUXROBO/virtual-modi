FROM python:3.6-slim-buster
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python setup.py install --user

EXPOSE 8765
CMD ["python", "run.py"]
