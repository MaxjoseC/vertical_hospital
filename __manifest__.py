{
    'name': 'Vertical Hospital',
    'version': '1.0',
    'author': 'Emanuel Crucel',
    'summary': 'Gestión de pacientes y tratamientos para hospitales',
    'description': """
        Módulo para gestión de pacientes, tratamientos y reportes en hospitales
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/paciente_views.xml',
        'views/tratamiento_views.xml',
        'views/res_config_settings_views.xml',
        'report/paciente_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}