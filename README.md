![test](https://github.com/Savetang19/ku-polls/actions/workflows/python-app.yml/badge.svg)
[![codecov](https://codecov.io/gh/Savetang19/ku-polls/branch/main/graph/badge.svg?token=FISD5KU7K8)](https://codecov.io/gh/Savetang19/ku-polls)
## Online Polls And Surveys
This is Web application for polls and surveys at Kasetsart University.  
App created as part of the [Individual Software Process](https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run
### Install instructions
Clone this repository by using this command on terminal
```
git clone https://github.com/Savetang19/ku-polls.git
```
DO NOT forget to change directory to projrct directory
```
cd ku-polls
```
Now, create a virtual environment,  
for **Mac/Linux** use this command
```
python -m venv env           # create the virtual env in "env/", only 1 time
. env/bin/activate           # start the virtual env in bash or zsh
```
for **Windows** use this command
```
python -m venv env
. .\env\Scripts\activate
```
Now, you have your own virtual evironment. Please install dependencies by following command
```
pip install -r requirements.txt
```
When you have all requirements packages. Then, create a new database by running migrations.
```
python manage.py migrate
```
Then import data using “loaddata”:
```
python manage.py loaddata data/polls.json data/users.json
```
### How to run
To run the server please use
```
python manage.py runserver
```

To deactivate the virtual environment:
```
deactivate
```

## Demo Users
You can log in to the site using the following account.
|Username| Password|
|:------:|:-------:|
|demouser1|demopass1|
|demouser2|demopass2|


## Project Documents
All project documents are in the [Project Wiki](../../wiki/Home)
* [Vision Statement](../../wiki/Vision%20Statement)
* [Requirements](../../wiki/Requirements)
* [Project Plan](../../wiki/Development%20Plan)
* [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
* [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
* [Iteration 3 Plan](../../wiki/Iteration%203%20Plan)
* [Iteration 4 Plan](../../wiki/Iteration%204%20Plan)
* [Task Board](../../projects)


[django-tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)
