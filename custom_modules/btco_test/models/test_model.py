from odoo import models, fields, Command, api
from odoo.exceptions import UserError
from odoo.osv.expression import OR, AND


class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'
    _order = 'name, age, id'
    _rec_name = 'age'

    name = fields.Char()
    age = fields.Integer()

    vendor_id = fields.Many2one('res.partner', string='Vendor')
    customer_ids = fields.Many2many('res.partner', string='Customers')

    parent_id = fields.Many2one('test.model', string='Parent', required=False)
    child_ids = fields.One2many('test.model', 'parent_id', string='Children')

    def method_a(self):
        return self.name

    @classmethod
    def method_b(cls):
        return cls._name

    def test_magic_numbers_0(self):
        # Start of transactions
        try:
            test = self.search([])  # works ok inside the same class
            test = self.env['test.model'].search([])  # works the same, but you specify the class
            test.write({'name': 'testing transactions'})
            test_2 = self.create({'name': "testing transactions 2", 'age': 22})
            test_2.unlink()
            print(test.name + test['name'])
            print(', '.join(record.name for record in test))
            self.env['test.model'].search([])
        except Exception as e:
            self.env.cr.rollback()
            raise e
        self.env.cr.commit()
        # End of transactions

    def test_magic_numbers(self):
        # transaction START
        records = self.browse([9, 10, 11])
        search_records = self.search([], limit=3, offset=2, sort='age desc')
        records_groups = {}
        for record in search_records:
            if record.vendor_id.name in records_groups:
                records_groups[record.vendor_id.name] += record.id
            else:
                records_groups[record.vendor_id.name] = record.ids

        return search_records.filtered_domain([('age', '>', 20)])
        pass

    # api.model implies that your method is designed to create ONE record at a time
    # @api.model
    # api.model implies that your method is designed to create MORE THAN ONE record at a time
    @api.model_create_multi
    def create(self, vals_list):  # You're overriding the existing method create
        for vals in vals_list:
            if 'parent_id' in vals_list:
                print('This record has a parent')
        return super(TestModel, self).create(vals_list)

    def write(self, vals):
        if 'parent_id' in vals:
            print("This record has a parent")
        return super().write(vals)

    def unlink(self):
        res = super().unlink()
        if self.age > 45:
            raise UserError("You cannot delete a record with age greater than 45")
        return res

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['name'] = 'Default name from default_get'
        return res

    def name_get(self):
        name_array = []
        for record in self:
            name_array.append((record.id, f"{record.name}, {record.age}"))
        return name_array

    def _name_search(self, value='', args=None, operator='like', limit=100, name_get_uid=None):
        domain = args or []
        if value:
            domain = OR([domain, ['|', ('name', operator, value), ('age', operator, value)]])
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)


