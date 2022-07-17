# Clone code
Clone the repo: git clone <repo name>
Create your local python virtual enviroment: - Run: python3 -m venv env - To activate the virtual python enviroment run: source env/bin/activate
Run pip install -r requirements.txt to install all python dependencies inside the virtual enviroment we will be developing on. See Errors section for help.
Create the .env file and add the content there

Using celery for ingest data on runserver

Celery Commands
celery -A main worker -l info # for async
celery -A main beat -l info # for scheduling

# Data Ingestion
On successful runserver, a asyncronous task is triggered through celery worker
this creates a client and connect it using the credentials provided to be saved in .env
Further topic is subscribed and data is ingested into our system. On ingestion, data is saved in
database and this functionality is looped on until celery is down.

# Web App
On traversing the url, login into the superuser account.
You see a meter list clicking on which you will see its details.
