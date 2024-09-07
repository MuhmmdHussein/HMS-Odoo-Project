from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'

    name = fields.Char()
    Capacity = fields.Integer()
    Is_opened = fields.Boolean()

