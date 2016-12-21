# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de productos sin stock' )
    q = db.producto.cantidad == 0
    grid = SQLFORM.grid(db(q),
                        create = False,
                        deletable = True,
                        editable=True,
                        details=True,
                        csv = True,
                        user_signature = False,
                        exportclasses = dict(cvs = False,
                                             xml = False,
                                             csv_with_hidden_cols = False,
                                             tsv_with_hidden_cols = False,
                                             tsv = False,
                                             json = False )
                       )
    return locals()




def admin():
    titulo = T(' Administración de productos' )
    grid = SQLFORM.grid(db.producto, deletable = False,
                            user_signature = False,
                            csv = True,exportclasses = dict(cvs = False,
                                                            xml = False,
                                                            csv_with_hidden_cols = False,
                                                            tsv_with_hidden_cols = False,
                                                            tsv = False,
                                                            json = False ))
    return locals()

def productosListados():
    tieneCompraVigente = False
    #try:
    categoria = request.args[0]
    titulo = tituloCategoria(categoria)
    detVenta = None

    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
        registro = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select().first()

        if registro is not None:
            tieneCompraVigente = True
            #print registro
            detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
            importeTotal = 0
            for row in detVenta:
                importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)
            idVenta = registro.id
            #print 'Importe Total:'+ str(importeTotal)
    #FIN - Verifica si tiene algo en el carrito#

    if request.vars.pagina is not None:
        pagina = int(request.vars.pagina)
    else:
        pagina = 0
    elementos_por_pagina = 9 if tieneCompraVigente else 10
    limitby = (pagina*elementos_por_pagina, (pagina+1)*elementos_por_pagina + 1)


    form = SQLFORM.factory(
        Field('nombre','string',label='Nombre:', default=(None if session.nombre is None else session.nombre)),
        Field('precioMenor','int', label='Precio desde:', default=(None if session.precioMenor is None else session.precioMenor)),
        Field('precioMayor','int', label='Precio hasta:', default=(None if session.precioMayor is None else session.precioMayor)),
        submit_button='Buscar')

    if form.process().accepted:
        query = armarQuery(form,categoria)
        productos = db(query).select(orderby = db.producto.precioVenta)#,limitby=limitby)
        response.flash = None
    else:
        productos = db((db.producto.categoria == categoria)&(db.producto.cantidad > 0)).select(orderby = db.producto.precioVenta,limitby=limitby)

    #except Exception as blumba:
        #print blumba
    return locals()


##Pantalla de Detalle de producto
def detalleProducto():
    try:
        tieneCompraVigente = False
        titulo = T('Detalle de producto')
        filtro = request.args[0]
        categoria = request.args[1]
        producto = db(db.producto.id == filtro).select().first()
        #print producto.varietal
        #varietal = db(db.varietal.id == producto.varietal).select(db.varietal.tipoVarietal)
        #print varietal.tipoVarietal
        tieneCompraVigente = False
        cantidad = 0
        precio = 0
        detVenta = None
        #Inicio -Verifica si tiene algo en el carrito#
        if auth.user:
            registro = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro is not None:
                tieneCompraVigente = True
                idVenta = registro.id
                #print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

                #print 'Importe Total:'+ str(importeTotal)
        #FIN - Verifica si tiene algo en el carrito#

    except Exception as blumba:
        print blumba
    return locals()
