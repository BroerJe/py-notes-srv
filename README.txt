#########################
#                       #
#  py-notes-srv ReadMe  #
#                       #
#########################

##
#  About
##

The py-notes-srv project implements a simple FastAPI backed python server 
which accepts HTTP requests for storing and retrieving UTF-8 notes. The notes 
are stored by UUID in a SQLite3 database.


##
#  Requirements
##

This project requires other packages to function. Use **venv** with the 
included **requirements.txt** to install all requirements in a self contained 
environment.

##
#  Container
##

This project includes a **Dockerfile** used to build a container for deployment.
This docker container will be built with the configurations found in the **res** 
directory.

For more information on the Dockerfile and container, check here:
https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi
https://docs.docker.com/storage/volumes/


##
#  Licence
##

This project is licenced under the GNU General Public V2.0 licence. 
Please read the included LICENCE.txt for the exact terms.


##
#  Directories
##

Directory List:
py-notes-srv: Project script files.
res: Project resource files.