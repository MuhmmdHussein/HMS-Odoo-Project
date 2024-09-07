from odoo import models, fields
from datetime import date

class AddState(models.TransientModel):
    _name = 'add.state'

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')])
    description = fields.Text(string='Description')
    patient_id = fields.Many2one('hms.patient', string="Patient", required=True)

    def action_confirm_wizard(self):
        self.ensure_one()
        # Update the patient state
        self.patient_id.write({
            'state': self.state
        })
        # Add log history
        self.env['hms.patient.line'].create({
            'date': date.today(),
            'created_by': self.env.user.id,
            'description': self.description,
            'patient_id': self.patient_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}