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
    form = SQLFORM.factory(
        Field('nombre','string',label='Nombre:', default=None),
        Field('precioMenor','integer', label='Precio desde:', default=0),
        Field('precioMayor','integer', label='Precio hasta:', default=None),
        Field('varietal', 'string',label='Varietal:', default=None),
        submit_button='Buscar')

    if form.process().accepted:
        query =  armaQuery(form)
        print query
        productos = db(query).select(orderby = db.producto.precioVenta)
        response.flash = None
    else:
        productos = db(db.producto.id>5711).select(orderby = db.producto.precioVenta)

    return locals()
def armaQuery(form = None):
    query=None
    if form.vars.nombre != None:
        query = db.producto.nombre.like('%'+form.vars.nombre+'%')
    print form.vars.precioMenor
    if form.vars.precioMenor != 0:
        if query != None:
            query &= ( db.producto.precioVenta >= form.vars.precioMenor )
        else:
            query = ( db.producto.precioVenta >= form.vars.precioMenor )

    return query

def comprarEste():
    titulo = "Próximamente"
    return locals()

def detalleProducto():
    titulo = T('Detalle de  producto')
    
    return locals()
