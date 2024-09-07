from odoo import fields, models, api, re
from odoo.exceptions import ValidationError
from datetime import date


class Patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    birth_date = fields.Date(string='Birth Date', required=True)
    history = fields.Html()
    CR_ratio = fields.Float(required=True)
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('o', 'O')])
    PCR= fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    log_history_id = fields.One2many('hms.patient.line', 'patient_id')
    department_id = fields.Many2one('hms.department', string='Department')
    doctor_id = fields.Many2one('hms.doctor', string='Doctor')
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.Capacity',
        readonly=True
    )
    Patient_line_ids = fields.One2many('hms.patient.line', 'patient_id')
    customer_id = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='User')



   # ========== Create a log History ==========

    @api.model
    def create(self, vals):
        res = super(Patient, self).create(vals)
        if 'state' in vals:
            self.env['hms.patient.line'].create({
                'date': date.today(),
                'created_by': self.env.user.id,
                'description': f'State changed to {vals.get("state")}',
                'patient_id': res.id
            })
        return res

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if 'state' in vals:
            for record in self:
                self.env['hms.patient.line'].create({
                    'date': date.today(),
                    'created_by': self.env.user.id,
                    'description': f'State changed to {vals.get("state")}',
                    'patient_id': record.id
                })
        return res



# ======== StatusBar =============


    step = fields.Selection([
        ('start', 'Start'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete')],
    )

    def action_start(self):
        for rec in self:
            rec.step = 'start'

    def action_progress(self):
        for rec in self:
            rec.step = 'in_progress'

    def action_complete(self):
        for rec in self:
            rec.step = 'complete'


# =========== Handling Wizard Action ==========

    def action_add_wizard(self):
        action = self.env['ir.actions.act_window']._for_xml_id('hospital_management_system.add_state_wizard_action')
        return action



# ====== Check if Email Vaild and Unique ======

    @api.onchange('email')
    def validation_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match is None:
                raise ValidationError('this Email Is Not Valid')

    @api.constrains('email')
    def _check_unique_email(self):
        for record in self:
            if self.search([('email', '=', record.email), ('id', '!=', record.id)]):
                raise ValidationError("Email address must be unique.")




# ========== Auto Calulate Age =============

    @api.depends('birth_date')
    def _compute_age(self):

        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0



# ============= Handling Log History ============

class PatientLine(models.Model):
    _name = 'hms.patient.line'
    _description = 'Patient Line'

    date = fields.Date(string='Date')
    created_by = fields.Many2one('res.users', string='Created By', readonly=True)
    description = fields.Text(string='Description')
    patient_id = fields.Many2one('hms.patient', string='Patient')  # Ensure this field is defined
