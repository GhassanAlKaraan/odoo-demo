from odoo import fields, models

class TestWizard(models.TransientModel):
    _name = "test.wizard"
    _description = "Test Wizard"

    name=fields.Char(string="Name")

    def validate(self):
        print("Wizard Name: %s" % self.name)

