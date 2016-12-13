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

        categoria = request.args(0) or redirect(URL('default', 'index'))
        titulo = tituloCategoria(categoria)

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
            productos = db(db.producto.categoria == categoria).select(orderby = db.producto.precioVenta)

        #Inicio -Verifica si tiene algo en el carrito#
        if auth.user:
            cantidad = db((db.venta.idCliente == auth.user.id) & (db.venta.estado != 'Pendiente')).count()
            print cantidad
            if cantidad != 0:
                tieneCompraVigente = True
                titulo2='Prueba / luego cambiar'
            else:
                tieneCompraVigente = False

        else:
            tieneCompraVigente = False
        #FIN - Verifica si tiene algo en el carrito#

    except Exception as blumba:
        print blumba
    return locals()

def comprarEste():
    titulo = "Próximamente"
    return locals()

def armarQuery(form = None, categoria = None):
    try:
        query=None
        print '1 - ' + form.vars.nombre
        print '2 - ' + form.vars.precioMenor
        print '3 - ' + form.vars.precioMayor
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

        print query
        query = isNoneConcat(query,(db.producto.categoria == categoria)&(db.producto.cantidad > 0))
    except Exception as blumba:
        print blumba
    return query

def isNoneConcat(resultado, consulta):
    if resultado != None:
        resultado &=  consulta
    else:
        resultado = consulta
    return resultado

##Pantalla de Detalle de producto
def detalleProducto():
    titulo = T('Detalle de producto')
    #filtro = request.args[0]
    filtro = 2931
    producto = db(db.producto.id == filtro).select().first()
    tieneCompraVigente = False
    return locals()
