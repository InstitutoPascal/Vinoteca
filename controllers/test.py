# -*- coding: utf-8 -*-
def index():
    try:

        db.venta.insert(idCliente = 4,
                        estado = 'Pendiente')

        print 'paso'
    except Exception as blumba:
        print blumba
    return tieneCompraVigente
