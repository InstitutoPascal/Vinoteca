# -*- coding: utf-8 -*-
def index():
    try:
        if auth.user:
            cantidad = db((db.venta.idCliente == auth.user.id) & (db.venta.estado != 'Pendiente')).count()
            print cantidad
            if cantidad != 0:
                tieneCompraVigente = True

            else:
                tieneCompraVigente = False

        else:
            tieneCompraVigente = False
        print tieneCompraVigente
    except Exception as blumba:
        print blumba
    return tieneCompraVigente
