FROM python:3.10
WORKDIR /app
COPY requirments.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirments.txt
COPY . /app/
CMD python3 /app/bot.py