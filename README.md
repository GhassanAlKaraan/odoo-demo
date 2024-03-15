# My first Odoo project

## Setup

**1- Prepare odoo sdk on your machine with python 3.10 :** [See How](https://www.odoo.com/documentation/15.0/administration/install/source.html)

-odoo-17.0 (*clone [odoo repo](https://github.com/odoo/odoo) and install requirements*) \
-Project Root Folder **You are here: C:\odoo-projects\Odoo** \
| \
|-- conf/odoo.conf \
|-- custom_modules \

**2- Prepare postgres database:**

*username = odoo,* \
*password = odoo,* \
*database = PostgreSQL*

## Run the server with configs

`python ..\odoo-17.0\odoo-bin -c ..\conf\odoo.conf`

**or using full path:**

`python C:\odoo-projects\Odoo\odoo-17.0\odoo-bin -c C:\odoo-projects\Odoo\conf\odoo.conf`

## Run server manually

`python cd ..\odoo-17.0\odoo-bin -r odoo -w odoo --addons-path=addons,..\custom_modules -d PostgreSQL`

**or run server in shell session:**

`python odoo-bin shell -r odoo -w odoo --addons-path=addons,..\custom_modules -d PostgreSQL`

## Scaffold a module

`python odoo-bin scaffold scaffolded_module C:\odoo-projects\Odoo\custom_modules`
