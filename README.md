# yelp_scraping
Scrapping Yelp website

## Project Structure

This is the folder/file structure we have.

```
/yelp_scraping
├── /yelp_project
│   ├── __init__.py             ----------------------------> Construct app here   
│   ├── constant.py             ----------------------------> All needed constants here(Not present currently)
│   └── /yelp_scrap
│       ├── __init__.py
│       ├── models.py            -------------> Business logic plus Database model
│       ├── routes.py            -------------> Defined the routes here
│       ├── constants.py            -------------> All the constants here
│       ├── custom_logger.py            -------------> Custom Logger file
│       ├── driver.py -------------> Driver classes for all the apis
│       ├── utils.py -------------> Utilities function
│       └── config.py            ------------------------> For cofiguration
└── requirements.txt        ------------------------> Packages and third party libraries
└── wsgi.py                 ------------------------> For running our app, This is entry point
└── .env                    ------------------------> For exporting secret variables
└── .gitignore              ------------------------> Listing all files/folders to ignore in git commits
```


### Project setup

#### Linux


```shell
$ git clone REPOSITORY_URL
$ cd FOLDER_NAME
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ flask run
```


### Database related stuff

1. Install Postgres

```shell
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get -y install postgresql # You can define specific version here
```

​		Please refer these links for more information

​		https://www.postgresql.org/download/linux/ubuntu/

​		https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

 2. Creating a database

    You should be able to create a database in postgres using *createdb* command, the database name you can keep it as you want. This database connection details is to be stored in **.env** file where we will store secrets. This file is in gitognore (What's the meaning of adding it in git, It's Top secret ;) ) 

    In that file there is this constant

    ```
    ENV_DEVELOPMENT_DB_URL='postgres://USERNAME:PASSWORD@localhost/DATABASE_NAME'
    ```

#### Sample .env

