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
    try:
        categoria = request.args[0]
        titulo = tituloCategoria(categoria)
        detVenta = None

        form = SQLFORM.factory(
            Field('nombre','string',label='Nombre:', default=None),
            Field('precioMenor','int', label='Precio desde:', default=None),
            Field('precioMayor','int', label='Precio hasta:', default=None),
            submit_button='Buscar')

        if form.process().accepted:
            query = armarQuery(form,categoria)
            productos = db(query).select(orderby = db.producto.precioVenta)
            response.flash = None
        else:
            productos = db((db.producto.categoria == categoria)&(db.producto.cantidad > 0)).select(orderby = db.producto.precioVenta)
        print '###################################################'
        #Inicio -Verifica si tiene algo en el carrito#
        if auth.user:
            registro = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro != None:
                tieneCompraVigente = True
                print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)
                idVenta = registro.id
                #print 'Importe Total:'+ str(importeTotal)
            else:
                tieneCompraVigente = False

        else:
            tieneCompraVigente = False
        #FIN - Verifica si tiene algo en el carrito#
        print tieneCompraVigente
    except Exception as blumba:
        print blumba
    return locals()


##Pantalla de Detalle de producto
def detalleProducto():
    try:
        titulo = T('Detalle de producto')
        filtro = request.args[0]
        categoria = request.args[1]
        producto = db(db.producto.id == filtro).select().first()
        tieneCompraVigente = True
        cantidad = 0
        precio = 0
        detVenta = None
        #Inicio -Verifica si tiene algo en el carrito#
        if auth.user:
            registro = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro != None:
                tieneCompraVigente = True
                print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

                print 'Importe Total:'+ str(importeTotal)
            else:
                tieneCompraVigente = False

        else:
            tieneCompraVigente = False
        #FIN - Verifica si tiene algo en el carrito#

    except Exception as blumba:
        print blumba
    return locals()
