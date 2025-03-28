from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime

class PacienteController(http.Controller):

    @http.route('/pacientes/consulta/<string:secuencia>', 
                type='http', 
                auth='none',  
                methods=['GET'], 
                cors='*')
    def consultar_paciente(self, secuencia, **kwargs):
        try:
            # Buscar paciente con filtro seguro
            paciente = request.env['hospital.paciente'].sudo().search([
                ('secuencia', '=', secuencia),
                ('estado', '!=', 'borrador') 
            ], limit=1)

            if not paciente:
                return Response(
                    json.dumps({'error': 'Paciente no encontrado o no disponible'}),
                    status=404,
                    mimetype='application/json'
                )
            
            # Estructura de respuesta exacta como en el PDF
            response_data = {
                "seq": paciente.secuencia,
                "name": f"{paciente.name} {paciente.apellido}",
                "rnc": paciente.rnc,
                "state": paciente.estado
            }
            
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                status=200,
                headers=[('Content-Type', 'application/json')]
            )
            
        except Exception as e:
            return Response(
                json.dumps({'error': 'Error en el servidor'}),
                status=500,
                mimetype='application/json'
            )