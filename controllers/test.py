# -*- coding: utf-8 -*-
def index():
    try:
        registro = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select().first()
        print registro
        if registro != None:
            tieneCompraVigente = True
            print 'tiene'
        else:
            print  'no tiene'

    except Exception as blumba:
        print blumba
    return locals()
