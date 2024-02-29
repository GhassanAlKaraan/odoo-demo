# My first Odoo project

## Setup

First, complete the odoo setup on your machine with python 3.10 \
[See How](https://www.odoo.com/documentation/15.0/administration/install/source.html)

Project Folder C:\odoo-projects\Odoo\ \
| \
|-- custom_modules \
|-- odoo-17.0 (*clone [odoo repo](https://github.com/odoo/odoo) and install requirements*)
|-- conf/odoo.conf

## Run the server with configs

`python odoo-bin -c C:\odoo-projects\Odoo\conf\odoo.conf`

## Run server manually

`cd odoo-17.0`

username = odoo, \
password = odoo, \
database = PostgreSQL \

`python odoo-bin -r odoo -w odoo --addons-path=addons,..\custom_modules -d PostgreSQL`

or Run server in shell session

`python odoo-bin shell -r odoo -w odoo --addons-path=addons,..\custom_modules -d PostgreSQL`

Querying examples:

`self.env['res.users'].browse(2)`
`self.env['res.users'].browse(2).name`

Apply changes to database:

`self.env.cr.commit()`

Scaffold a module:

`python odoo-bin scaffold scaffolded_module C:\odoo-projects\Odoo\custom_modules`
