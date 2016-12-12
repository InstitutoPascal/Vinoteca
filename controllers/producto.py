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
        form = SQLFORM.factory(
            Field('nombre','string',label='Nombre:', default=None),
            Field('precioMenor','int', label='Precio desde:', default=None),
            Field('precioMayor','int', label='Precio hasta:', default=None),
            Field('varietal', label='Varietal:', requires= IS_EMPTY_OR(IS_IN_DB(db,db.varietal,'%(tipoVarietal)s', zero=''))),
            submit_button='Buscar')

        if form.process().accepted:
            query = armarQuery(form,categoria)
            productos = db(query).select(orderby = db.producto.precioVenta)
            response.flash = None
        else:
            productos = db(db.producto.categoria == categoria).select(orderby = db.producto.precioVenta)

    except Exception as blumba:
        print blumba
    return locals()

def comprarEste():
    titulo = "Próximamente"
    return locals()

def detalleProducto():
    titulo = T('Detalle de  producto')
    producto = request.args[0]
    registro = db(db.producto.id == producto).select()
    return locals()

def armarQuery(form = None, categoria = None):
    try:
        query=None
        print '1' + form.vars.nombre
        print '2' + form.vars.precioMenor
        print '3' + form.vars.precioMayor
        if form.vars.nombre != '':
            query = (db.producto.nombre.like('%'+form.vars.nombre+'%'))

        if form.vars.precioMenor != '' and form.vars.precioMayor != '':
            query = isNoneConcat(query,(db.producto.precioVenta >= form.vars.precioMenor) & (db.producto.precioVenta <= form.vars.precioMayor))
        elif form.vars.precioMenor != '':
            query = isNoneConcat(query,(db.producto.precioVenta >= form.vars.precioMenor))
        elif form.vars.precioMayor != '':
            query = isNoneConcat(query,(db.producto.precioVenta <= form.vars.precioMayor))
        else:
            pass

        if form.vars.nombre != '':
            query = (db.producto.nombre.like('%'+form.vars.nombre+'%'))

        print query
        query = isNoneConcat(query,db.producto.categoria == categoria)
    except Exception as blumba:
        print 'No le gusto:' + blumba
    return query

def isNoneConcat(resultado, consulta):
    if resultado != None:
        resultado &=  consulta
    else:
        resultado = consulta
    return resultado
