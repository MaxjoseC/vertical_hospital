from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Paciente(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True, tracking=True)
    apellido = fields.Char(string='Apellido', required=True, tracking=True)
    secuencia = fields.Char(string='N° Expediente', readonly=True, copy=False, default='New')
    rnc = fields.Char(string='RNC', required=True, tracking=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('alta', 'Alta'),
        ('baja', 'Baja')
    ], string='Estado', default='borrador', tracking=True, required=True)
    fecha_alta = fields.Datetime(string='Fecha de Alta', default=fields.Datetime.now, readonly=True)
    fecha_actualizacion = fields.Datetime(string='Última Actualización', compute='_compute_actualizacion', store=True, readonly=True)
    tratamientos_ids = fields.Many2many(
        'hospital.tratamiento',
        string='Tratamientos',
        relation='paciente_tratamiento_rel',
        column1='paciente_id',
        column2='tratamiento_id'
    )

    @api.depends('write_date')
    def _compute_actualizacion(self):
        for record in self:
            record.fecha_actualizacion = fields.Datetime.now()

    @api.constrains('rnc')
    def _check_rnc(self):
        for record in self:
            if record.rnc and not record.rnc.isdigit():
                raise ValidationError("El RNC solo debe contener números")

    @api.model
    def create(self, vals):
        if vals.get('secuencia', 'New') == 'New':
            vals['secuencia'] = self.env['ir.sequence'].next_by_code('hospital.paciente') or 'New'
        return super().create(vals)

    def action_confirmar_alta(self):
        for record in self:
            if record.estado == 'borrador':
                record.estado = 'alta'
        return True

    def action_dar_baja(self):
        for record in self:
            if record.estado == 'alta':
                record.estado = 'baja'
        return True

    def action_reabrir(self):
        for record in self:
            if record.estado == 'baja':
                record.estado = 'alta'
        return True
    def action_print_report(self):
        return self.env.ref('vertical_hospital.action_report_paciente').report_action(self.id)