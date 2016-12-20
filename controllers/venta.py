# -*- coding: utf-8 -*-
##Listado del vendedor##
def index():
    form = SQLFORM.factory(
            Field('fechaDesde','date', label='Fecha desde:', default=None),
            Field('fechaHasta','date', label='Fecha hasta:', default=None),
            Field('estado','string', label='Estado:', default=None, requires=IS_EMPTY_OR(IS_IN_SET(["Pendiente", "Finalizado", "Pendiente confirmar fecha", "Delivery", "Retira", "Entergado"]))),
            submit_button='Buscar')

    if form.process().accepted:
        response.flash = None
        query = armarQueryVentas(form)
        grid = SQLFORM.grid(query,
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) )),
                                     dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) ))])
    else:
        grid = SQLFORM.grid(db.venta,
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) )),
                                     dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) ))])
    return locals()

##################

def mostrarVenta():
    idVenta = request.args[0]

    detVenta = db((db.detalleVenta.idVenta == idVenta)&(db.producto.id==db.detalleVenta.idProducto)).select()
    importeTotal = 0
    for row in detVenta:
        importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

    formVenta = SQLFORM(db.venta, idVenta)

    return locals()



