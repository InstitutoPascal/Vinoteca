# -*- coding: utf-8 -*-
def index():
    try:
        idVenta = request.args[0]
        db(db.detalleVenta.id == idVenta).delete()
        db(db.venta.id == idVenta).delete()
        if registro != None:
            tieneCompraVigente = True
            print 'tiene'
        else:
            print  'no tiene'

    except Exception as blumba:
        print blumba
    return locals()


def listaProds():

    if len(request.args): pagina=int(request.args[0])
    else: pagina=0
    elementos_por_pagina=20
    limitby=(pagina*elementos_por_pagina, (pagina+1)*elementos_por_pagina+1)
    registros=db().select(db.producto.ALL, limitby=limitby)
    categoria = 2
    return locals()
