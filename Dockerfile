FROM python:3
WORKDIR /usr/src/app
ADD ./requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD ./main.py main.py
COPY ./app app
COPY ./database database
COPY ./routers routers
COPY ./controllers controllers
COPY ./utils utils
VOLUME /app
VOLUME /routers
EXPOSE 8001
CMD ["python3", "main.py"]