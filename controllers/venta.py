# -*- coding: utf-8 -*-
##Listado del vendedor##
def index():
    form = SQLFORM.factory(
        Field('cliente','string', label='Cliente:', default=None, requires=IS_EMPTY_OR(IS_IN_DB(db, 'auth_user.id',
                                                                                                '%(first_name)s - %(last_name)s'))),
        Field('fechaDesde','date', label='Fecha desde:', default=None),
        Field('fechaHasta','date', label='Fecha hasta:', default=None),
        Field('estado','string', label='Estado:', default=None, requires=IS_EMPTY_OR(IS_IN_SET(["Pendiente", "Finalizado",
                                                                                                "Pendiente confirmar fecha",
                                                                                                "Delivery", "Retira", "Entergado"]))),
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
                            csv = True,
                            user_signature = False,
                            exportclasses = dict(cvs = False,
                                                 xml = False,
                                                 csv_with_hidden_cols = False,
                                                 tsv_with_hidden_cols = False,
                                                 tsv = False,
                                                 json = False ),
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) )),
                                     dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default",
                                                                        _href=URL('venta','editarVenta/%s'%row.id) ))])
    else:
        grid = SQLFORM.grid((db.venta.formaEntrega != None),
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = True,
                            user_signature = False,
                            exportclasses = dict(cvs = False,
                                                 xml = False,
                                                 csv_with_hidden_cols = False,
                                                 tsv_with_hidden_cols = False,
                                                 tsv = False,
                                                 json = False ),
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('venta','mostrarVenta/%s'%row.id) )),
                                     dict(header=' ',body=lambda row: A('Modificar',_class="button btn btn-default",
                                                                        _href=URL('venta','editarVenta/%s'%row.id) ))])
    return locals()

##################

def mostrarVenta():
    idVenta = request.args[0]
    detVenta = db((db.detalleVenta.idVenta == idVenta)&(db.producto.id==db.detalleVenta.idProducto)).select()
    importeTotal = 0
    for row in detVenta:
        importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

    formVenta = SQLFORM(db.venta,  idVenta, readonly=True)

    return locals()

###################

def editarVenta():
    idVenta = request.args[0]

    detVenta = db((db.detalleVenta.idVenta == idVenta)&(db.producto.id==db.detalleVenta.idProducto)).select()
    importeTotal = 0
    for row in detVenta:
        importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

    venta = db.venta(idVenta)
    form = SQLFORM(db.venta, venta)
    form.add_button('Eliminar venta',"javascript:return confirmarEliminar('%s', this);" %URL('venta','index'))
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('venta','index'))

    if form.process().accepted:
        if (form.vars.fechaEntrega is not None) and (venta.estado == 'Pendiente'):
            #envio mail
            session.flash = "Modificado correctamente. Email enviado."
            redirect(URL('venta', 'index'))
        else:
            session.flash = "Modificado correctamente"
            redirect(URL('venta', 'index'))
    elif form.errors:
        response.flash=' Complete el formulario '
    else:
        pass

    return locals()
