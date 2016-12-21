# -*- coding: utf-8 -*-
@auth.requires_membership('Desarrollador')
def index():
    try:
        idVenta = request.args[0]
        db(db.detalleVenta.id == idVenta).delete()
        db(db.venta.id == idVenta).delete()
        if registro is not None:
            tieneCompraVigente = True
            print 'tiene'
        else:
            print  'no tiene'

    except Exception as blumba:
        print blumba
    return locals()

@auth.requires_membership('Desarrollador')
def listaProds():
    '''if request.vars.pagina is not None:
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

def mailo():
    try:
        idVenta = 8
        detVenta = db((db.detalleVenta.idVenta == idVenta )&(db.producto.id==db.detalleVenta.idProducto)).select()
        print detVenta
        importeTotal = 0
        print "pasa"
        for row in detVenta:
            print "for"
            importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)
            print str(importeTotal)

        print "Sale del puto for"
        venta = db(db.venta.id == idVenta).select().first()
        print venta
        usuario = db.auth_user(venta.idCliente)
        print usuario
        print venta.fechaEntrega.strftime("%d/%m/%y")

        context = dict()
        context['nombre'] = usuario.first_name
        context['consultaSugerencia'] = "texto"
        context['fecha'] = "fecha"

        message = response.render('venta/emailDelivery.html', context)

        result = mail.send(to="villan.laura@gmail.com", subject='Su pedido fué procesado', message=message, headers=dict(contentType='text/html; charset="UTF-8"'))
        if result:
            print 'se envio'
        else:
            print 'no se envio'
    except Exception, e:
        print 'Fallo: %s' % e
    else:
        print 'sin problemas'
    return idVenta
