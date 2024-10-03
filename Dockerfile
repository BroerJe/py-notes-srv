##
#  Base
#  ----
#  py-notes-srv was written for Python 3.12.5, use as base.
##
FROM python:3.12.5

##
#  Create Project
#  --------------
#  We create the application directory in the container
#  and set up the requirements.
##
WORKDIR /py-notes-srv
COPY ./requirements.txt /py-notes-srv/requirements.txt
RUN pip3 install -r requirements.txt

##
#  Copy Content
#  ------------
#  We need to copy the docker content to run the service.
##
COPY ./src /py-notes-srv/src
#COPY ./res/configuration.json /var/py-notes-srv/configuration.json

##
#  User Storage
#  ------------
#  We now add the service file directory to allow notes storage.
##
RUN mkdir -p /var/py-notes-srv

##
#  Environment Variables
#  ---------------------
#  Add environment variables for configurations, etc.
##
ENV PY_NOTES_SRV_HOST="127.0.0.1"
ENV PY_NOTES_SRV_PORT=8000
ENV PY_NOTES_SRV_CONFIGURATION="/var/py-notes-srv/configuration.json"

##
#  Run
#  ---
#  The command(s) used when running the container.
#
#  --host: Set to 0.0.0.0 to accept incoming connections from all IPs.
#  --port: The port to listen on for connections.
##
WORKDIR /py-notes-srv
CMD uvicorn src.main:app --host $PY_NOTES_SRV_HOST --port $PY_NOTES_SRV_PORT