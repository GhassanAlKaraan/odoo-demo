# My first Odoo project

## Steps

You need to setup odoo-17.0 with python3.10 on your machine first \
[See How](https://www.odoo.com/documentation/15.0/administration/install/source.html)

Project Folder (C:\Odoo\) \
| \
|-- gts-btco (custom module) \
|-- odoo-17.0 (*clone odoo repo and install requirements*)

### Enter the odoo repo directory

` cd odoo-17.0 `

### Run local server + add custom module

` python odoo-bin -r odoo -w odoo --addons-path=addons,C:\Odoo\gts-btco -d PostgreSQL `

### Run server in shell session

` python odoo-bin shell -r odoo -w odoo --addons-path=addons,C:\Odoo\gts-btco -d PostgreSQL `

Querying examples:

`self.env['res.users'].browse(2)`
`self.env['res.users'].browse(2).name`

Apply changes to database:

`self.env.cr.commit()`

### Scaffold a module

`python odoo-bin scaffold scaffolded_module C:\Odoo\gts-btco`
