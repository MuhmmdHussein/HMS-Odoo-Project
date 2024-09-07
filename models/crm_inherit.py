from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Customer(models.Model):
    _inherit = 'res.partner'
    related_patient_ids = fields.One2many('hms.patient', 'customer_id')

    @api.constrains('email')
    def _check_email_in_patient_model(self):
        for record in self:
            if record.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', record.email)], limit=1)
                if existing_patient:
                    raise ValidationError("This email address already exists in the patient model.")

    def unlink(self):
        for record in self:
            if record.related_patient_ids:
                raise UserError("Cannot delete this customer because it is linked to one or more patients.")
        return super(Customer, self).unlink()

    vat = fields.Char(
        required=True,
    )
