FROM python:3
WORKDIR /usr/src/app
ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD ./main.py main.py
COPY ./app app
COPY ./database database
COPY ./routers routers
EXPOSE 8001
CMD ["python3", "main.py"]