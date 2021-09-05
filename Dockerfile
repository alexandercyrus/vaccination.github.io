# download a python image named 3.9-slim-buster from docker hub. With this image does have mostly needed python libraries and python itself.  
FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True

# create a variable
ENV APP_HOME /app
# set work directory as $APP_HOME
WORKDIR $APP_HOME
# if image builder is run within the directory which contains app files, this will copy all files from this dir to $APP_HOME dir. Since the deployment
# machines are linux machines the file structure is also linux
COPY . ./

# if there are many customized libraries which are not in 3.9-slim-buster, you can create a list of the required libraries in the requirement 
# file and install them. Python editors have plugins for this
#RUN pip3 install -r requirements.txt

# expose a specific port of container for your webapp otherwise your container by defalut does not accept http requests.
EXPOSE 8081

# run your main python program. Note there is a contianer port and there is a local machine port. the http requests first reach the machine and then
# the container. There should be an instruction for bing these two together at runtime. Here the container port is 8081. When deplying the image on 
# a cloud service this port should be given otherwise the app does not run or load.  
# -m flag makes .py extention for the python file price_analysis forbidden
CMD [ "python3", "-m" , "kepler","run", "--host=0.0.0.0", "-p","8081:8081"]
#CMD [ "python3", "-m" , "kepler", "run", "--host=0.0.0.0"]