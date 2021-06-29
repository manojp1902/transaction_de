FROM python:3.7

WORKDIR /appsource
COPY ./ /appsource
ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "app.py"]