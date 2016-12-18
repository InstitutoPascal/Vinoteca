# -*- coding: utf-8 -*-
@auth.requires_membership('Desarrollador')
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

@auth.requires_membership('Desarrollador')
def listaProds():
    '''if request.vars.pagina != None:
        pagina = int(request.vars.pagina)
    else:
        pagina = 0
    elementos_por_pagina = 5
    limitby = (pagina*elementos_por_pagina, (pagina+1)*elementos_por_pagina + 1)
    registros = db().select(db.producto.ALL, limitby=limitby)
    categoria = 2
    ## -  Date
    import datetime
    x = datetime.datetime.now()

    dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', 'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}
    anho = x.year
    mes =  x.month
    dia= x.day

    fecha = datetime.date(anho, mes, dia)
    print (dicdias[fecha.strftime('%A').upper()])'''
    grid = SQLFORM.smartgrid(db.venta, linked_tables=['detalleVenta'],
     searchable= dict(venta=True, detalleVenta=False))
    return locals()
