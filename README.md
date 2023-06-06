# yelp_scraping
Scrapping Yelp website

## Project Structure

This is the folder/file structure we have.

```
/yelp_scraping
├── /yelp_project
│   ├── __init__.py             ----------------------------> Construct app here   
│   ├── constant.py             ----------------------------> All needed constants here(Not present currently)
│   ├── response_utils.py       ----------------------------> Response utilities Success/Error(Not present currently)
│   ├── error_handler_utils.py  ----------------------------> App level error handler(Not present currently)
│   └── /yelp_scrap
│       ├── __init__.py
│       ├── models.py            -------------> Business logic plus Database model(TODO)
│       ├── routes.py            -------------> API endpoints(TODO)
│       ├── request_response_handler.py -------------> Managing the Requsts and final Response(Not present currently)
│       └── config.py            ------------------------> For cofiguration Production Vs Debug etc.(TODO)
└── tests
     ├── __init__.py
     ├── test_app.py        ------------------------> Test cases for all apis - For Pytest(Not Present currently)
└── flask_best_practices.wsgi  ------------------------> For deployment in apache(Not present currently)
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

## Packages used

##### python-dotenv

- [Package link](https://pypi.org/project/python-dotenv/)
- It would be annoying to set environment variables every time we open our terminal, so we can set environment variables in a local file called **.env** instead and grab those variables using a Python library like python-dotenv.
