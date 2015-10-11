## Cant Keep Up

[![Build Status](https://travis-ci.org/omarayad1/cantkeepup.svg)](https://travis-ci.org/omarayad1/cantkeepup)

This tool is made to make programmers more productive through issuing commands
via the address bar of their favorite browser.

## How to enable it in chrome
goto `settings` then under the `search` section press `Manage search engines`
now we will add cantkeepup here, scroll down until you find 3 empty boxes. In
the first box `Add a new search engine` type `cantkeepup`. In the second box
`Keyword` type `cantkeepup`. In the last box `URL with %s in place of query` 
type `http://cantkeepup.herokuapp.com/?q=%s`. Then press enter, and make it 
the default one by pressing the `Make default` button that appears when you 
hover over it.

ENJOY~~!

## How to build
first of all you need both pip and python2 installed then navigate to the 
project directory and issue the following commands:
```sh
$ pip install -r requirements.txt
$ python main.py
```

In order to be able to develop locally at your machine make sure you are running
your own psql server with a database named cantkeepup_dev, and having
`virtualenvwrapper` installed, and `$VIRTUAL_ENV/bin/postactivate` contains:
```sh
#!/bin/zsh
# This hook is sourced after this virtualenv is activated.
export APP_SETTINGS=config.DevelopmentConfig

# this assumes you have posgresql server installed locally, and you have
# a db named cantkeepup_dev already created.
export DATABASE_URL=postgresql://localhost/cantkeepup_dev
```

You will need to run the 'db_create.py' once in order to populate your local db.
```sh
$ python db_create.py
````

## Making changes to the database
We are using Flask-Migrate, and it can be done in a couple of easy steps. First,
make your changes to the models, then from the terminal issue this command:
`python manage.py migrate` and then `python manage.py upgrade`. To check what 
exactly happens check the function `upgrade` in the last created file in 
`cantkeeup-directory/migrations/versions`. As for moving or deleting the data
you have to do it yourself, either manually or automatically.

## Currently available functions
* `ocvs  <keywords>` --- search in OpenCV codebase in github
* `s <keywords>` or `g <keywords>` --- search using google
* `t <keywords>` --- translate from English to Arabic using google translate
* `p` --- redirect to pastie.org
* `ulib <keywords>` --- search AUC library
* `<keywords>` --- search using google (this is the default case by the way)
