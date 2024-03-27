# My Odoo project

## Setup on Windows

**1- Prepare odoo sdk on your machine with python 3.10 :**

a. Create a folder C:/Odoo/ and navigate to it\
b. Clone odoo repo: `git clone https://github.com/odoo/odoo.git` \
c. Create a python venv in C:/Odoo/odoo-17.0, and [install requirements](https://www.odoo.com/documentation/15.0/administration/install/source.html)

**2- Prepare postgres database:**

*username = odoo,* \
*password = odoo,* \
*database = PostgreSQL*

## Run the server

Note: You have to fix the paths in the config file, then run a command inside this project's directory:

### Run server in command line

`python C:\Odoo\odoo-17.0\odoo-bin -c .\conf\odoo.conf`

### Run server in shell session:

`python C:\Odoo\odoo-17.0\odoo-bin shell -c .\conf\odoo.conf`

### Run without the config file:

`python C:\Odoo\odoo-17.0\odoo-bin -r odoo -w odoo --addons-path=addons,.\custom_modules -d PostgreSQL`

## Get started

Scaffold a module:

`python odoo-bin scaffold scaffolded_module .\custom_modules`

*Happy Coding.*
