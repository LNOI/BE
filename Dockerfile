FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN apt-get update
# Install pip requirements
RUN python -m pip install pip setuptools wheel
COPY . /app
WORKDIR /app

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Install opencv dependencies
CMD ["/bin/bash"]
