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

I added those credentials to conf/odoo.conf

## Run the server

`python C:\Odoo\odoo-17.0\odoo-bin -c .\conf\odoo.conf`

Or run server in shell session:

`python C:\Odoo\odoo-17.0\odoo-bin shell -c .\conf\odoo.conf`

Or run **without** the config file:

`python C:\Odoo\odoo-17.0\odoo-bin -r odoo -w odoo --addons-path=addons,.\custom_modules -d PostgreSQL`

## Get started

Scaffold a module:

`python odoo-bin scaffold scaffolded_module C:\odoo-projects\Odoo\custom_modules`
