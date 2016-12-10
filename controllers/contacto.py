# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# intente algo como


def index():
    '''TODO: luego agregar los datos de contacto es un fromularion con consultas
    Bukino Vinoteca
    Tel: 011-4951-2236
    Cel:15-4787-7909
    '''
    grid = SQLFORM.grid(contacto)
    titulo = 'Consultas o sugerencias'
    return locals()

#@auth.requires_login()
def admin():
    grid = SQLFORM.grid(contacto)
    titulo = 'Consultas o sugerencias'
    return locals()
