FROM python:3.9-alpine
LABEL authors="thesharque"

ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /bot
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY *.py ./
ENTRYPOINT ["python", "hamster_bot.py"]
