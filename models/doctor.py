from odoo import fields, models


class Doctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "first_name"


    first_name = fields.Char()
    last_name = fields.Char()
    img = fields.Binary()
    department_id = fields.Many2one('hms.department', string='Department')
