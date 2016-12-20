# -*- coding: utf-8 -*-

def index():
    form = SQLFORM.factory(
            Field('fechaDesde','date', label='Fecha desde:', default=None),
            Field('fechaHasta','date', label='Fecha hasta:', default=None),
            Field('estado','string', label='Estado:', default=None, requires=IS_EMPTY_OR(IS_IN_SET(["Pendiente", "Finalizado", "Pendiente confirmar fecha", "Delivery", "Retira", "Entergado"]))),
            submit_button='Buscar')

    if form.process().accepted:
        response.flash = None
        query = armarQueryCompra(form,db.venta.idCliente == auth.user.id)
        grid = SQLFORM.grid(query,
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default", _href=URL('compra','mostrarCompraRealizada/%s'%row.id) )),dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default", _href=URL('compra','mostrarCompraRealizada/%s'%row.id) ))])
    else:

        grid = SQLFORM.grid((db.venta.idCliente == auth.user.id),
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default", _href=URL('compra','mostrarCompraRealizada/%s'%row.id) )),dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default", _href=URL('compra','mostrarCompraRealizada/%s'%row.id) ))])
    return locals()

#Listado del Usuario - podrá consultar #
def listadoCompras():

    form = SQLFORM.factory(
            Field('fechaDesde','date', label='Fecha desde:', default=None),
            Field('fechaHasta','date', label='Fecha hasta:', default=None),
            Field('estado','string', label='Estado:', default=None, requires=IS_EMPTY_OR(IS_IN_SET(["Pendiente", "Finalizado", "Pendiente confirmar fecha", "Delivery", "Retira", "Entergado"]))),
            submit_button='Buscar')

    if form.process().accepted:
        response.flash = None
        query = armarQueryCompra(form,db.venta.idCliente == auth.user.id)
        grid = SQLFORM.grid(query,
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default", _href=URL('venta','mostrarCompraRealizada/%s'%row.id) ))])
    else:

        grid = SQLFORM.grid((db.venta.idCliente == auth.user.id),
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default", _href=URL('venta','mostrarCompraRealizada/%s'%row.id) ))])
    return locals()

def mostrarCompraRealizada():
    idVenta = request.args[0]
    # = db(db.venta.id == idVenta).select().first()
    detVenta = db((db.detalleVenta.idVenta == idVenta)&(db.producto.id==db.detalleVenta.idProducto)).select()
    importeTotal = 0
    for row in detVenta:
        importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

    formVenta = SQLFORM(db.venta,  idVenta, readonly=True)

    return locals()
