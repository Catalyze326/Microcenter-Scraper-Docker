#RUN /opt/bin/generate_config > /opt/selenium/config.json
FROM python:3.8
# set the working directory in the container
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
COPY main.py .
# command to run on container start
CMD [ "python", "./main.py" ]

EXPOSE 4444