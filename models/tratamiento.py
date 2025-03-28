from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tratamiento(models.Model):
    _name = 'hospital.tratamiento'
    _description = 'Tratamiento'

    codigo = fields.Char(string='Código', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    medico = fields.Char(string='Médico Tratante')
    paciente_ids = fields.Many2many(
        'hospital.paciente',
        string='Pacientes',
        relation='paciente_tratamiento_rel',
        column1='tratamiento_id',
        column2='paciente_id'
    )
    #limitar codigo para que no pueda contener la secuencia 026
    @api.constrains('codigo')
    def _check_codigo(self):
        for record in self:
            if record.codigo and '026' in record.codigo:
                raise ValidationError("El código no puede contener la secuencia '026'")