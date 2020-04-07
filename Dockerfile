#иногда пишут версию ubuntu
FROM python:3.6.9

#создается папка
RUN mkdir -p /home/app/

#куда будет установлено изображение
WORKDIR /home/app

#передает файлы с компьютера в файловую систему контейнера
COPY requirements.txt requirements.txt

#RUN эквиволентна командной строке
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000
