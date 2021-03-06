# -*- coding: utf-8 -*-
# guarda en el carrito el producto ingresado
def impactarProducto():
#    try:
    producto = request.vars.idProducto
    cantidad = request.vars.cantidad
    categoria = request.vars.categoria
    if auth.user:
        if cantidad == 0:
            #print 'fallo cantidad = cero'
            session.flash = 'Verifique la cantidad que quiso inresar.'
            redirect(URL('producto', 'productosListados/%s'%categoria ))
        else:
            if tieneVentaVigente(auth.user.id):
                #do update
                #print 'tiene'
                ventaVigente = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select(db.venta.id).first()
                existe = db((db.detalleVenta.idVenta == ventaVigente)&(db.detalleVenta.idProducto == producto)).count()
                #print existe
                if existe > 0:
                    #print 'tiene en el carrito'
                    db((db.detalleVenta.idVenta == ventaVigente)&(db.detalleVenta.idProducto == producto)).update(cantidad = cantidad)
                    session.flash = 'El articulo ya se encuentra en el carrito. Se actualizó la cantidad requerida.'
                else:
                    resultadoDet = db.detalleVenta.insert(idVenta = ventaVigente, idProducto = producto, cantidad = cantidad)
                    if resultadoDet is not None:
                        #print 'insertó'
                        session.flash = 'Artículo agregado al carrito de compra.'
                redirect(URL('producto', 'productosListados/%s'%categoria ))
            else:
                #do inserts venta- detalle
                #print 'no tiene venta vigente'
                resultado = db.venta.insert(idCliente = auth.user.id, estado = 'Pendiente')
                #print resultado
                if resultado  is not None:
                    resultadoDet = db.detalleVenta.insert(idVenta = resultado, idProducto = producto, cantidad = cantidad)
                    if resultadoDet  is not None:
                        #print 'insertó'
                        session.flash = 'Artículo agregado al carrito de compra.'
                    else:
                        session.flash = 'Falló al  agregarlo.'

                    redirect(URL('producto', 'productosListados/%s'%categoria ))
                else:
                    #print 'fallo'
                    session.flash = 'Ocurrió un error al intentar guardar el producto en el carrito.'
                    redirect(URL('producto', 'productosListados/%s'%categoria ))


    else:
        #print 'Fallo'
        session.flash = 'Intentó realizar una acción que requiere que se encuentre logueado.'
        redirect(URL('producto', 'productosListados/%s'%categoria ))


    return locals()

#valida la existencia de un domicilio
def validateDomicilio(form):
    formaPago = form.vars.formaPago
    formaEntrega = form.vars.formaEntrega
    domiEntrega = form.vars.idDomicilio

    if formaEntrega is None:
        form.errors.formaEntrega = "Debe seleccionar una forma de entrega."
    if (formaEntrega == "Entrega a domicilio") and (domiEntrega is None):
        form.errors.idDomicilio = "Para *Entrega a domicilio* se requiere un domicilio."
    else:
        pass

#Listado de detalle de compra habilita finalizar o volver
def detalleCompraCliente():
    #print 'Detalle venta Cliente'
    idVenta = request.args[0]
    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
        cantDomicilio = db(db.domicilio.idCliente == auth.user.id).count()
        if (cantDomicilio is not None)&(cantDomicilio > 0 ) :
            registro = db((db.venta.id == idVenta) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro is not None:
                idVenta = registro.id
                #print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)
                consultaCombo = db.domicilio.idCliente == auth.user.id
                form  = SQLFORM.factory(
                    Field("formaPago", label=T('Forma de pago'), requires=IS_IN_DB(db,db.formaPago.id, '%(descripcion)s',
                                                                                   zero='Seleccionar',error_message="Ingrese una forma de pago.")),
                    Field("formaEntrega", 'string',  label=T('Forma de entrega'), requires=IS_EMPTY_OR(IS_IN_SET(["Acordar con el vendedor",
                                                                                                                  "Entrega a domicilio",
                                                                                                                  "Retira en local"]))),
                    Field("idDomicilio", label=T('Domicilio'), requires=IS_EMPTY_OR(IS_IN_DB(db(consultaCombo), db.domicilio.id,
                                                                                             '%(calle)s - %(numero)s - %(idZona)s'))),
                    submit_button='Confirmar Compra')

                form.add_button('Cancelar',
                                "javascript:return confirmarCancelar('%s', this);"
                                %URL('producto','productosListados/%s'
                                     %(request.vars.idCategoria if request.vars.idCategoria is not None else 1)))
                if form.process(onvalidation=validateDomicilio).accepted:
                    impactarCompra(idVenta,importeTotal,form)
                    redirect(URL('compra', 'mostrarCompraRealizada/%s' %idVenta))
                else:
                    pass
            else:
                response.flash = "Falló al obtener la compra."
                redirect(URL('default', 'index' ))
        else:
            #Redirigir a administracion de Domicilio
            session.flash = "Debe cargar un domicilio antes de continuar con la compra."
            redirect(URL('usuario', 'listarDirecciones' ))
    else:
        response.flash = "Usuario no logueado."
        redirect(URL('default', 'index' ))
    #FIN - Verifica si tiene algo en el carrito#
    return locals()

#Cancela la compra que se encuentra en el carrito
def cancela():
    #print 'Paso - Cancela compra'
    idVenta = request.args[0]
    #print idVenta
    db(db.detalleVenta.idVenta == idVenta).delete()
    db(db.venta.id == idVenta).delete()
    redirect(URL('default', 'index' ))
    return locals()

def eliminar():
    #print "pasa... que hace?"
    idProducto = request.args[0]
    idVenta = request.args[1]
    #print idProducto
    #print idVenta
    res =db((db.detalleVenta.idVenta == idVenta) & (db.detalleVenta.idProducto ==idProducto)).delete()
    #print res
    contar = db(db.detalleVenta.idVenta == idVenta).count()
    print contar
    if contar == 0:
        res = db(db.venta.id == idVenta).delete()
        print res
        session.flash = "Se eliminó toda la compra"
        redirect(URL('default', 'index' ), client_side=True)

    response.flash = 'Eliminado'
    return True

#Finaliza la compra por parte del cliente
def impactarCompra(idVenta,importe,form):
    try:
        #print 'ingresa'
        productosVendidos = db(db.detalleVenta.idVenta == idVenta).select()
        #print productosVendidos
        for prodVendido in productosVendidos:
            #print prodVendido.idProducto
            producto = db(db.producto.id == prodVendido.idProducto).select().first()
            #print "pasa a borrar"
            #print prodVendido.idProducto
            stock = producto.cantidad-prodVendido.cantidad
            #db(db.producto.id == prodVendido.idProducto).update(cantidad = stock)
            #descomentar la linea de arriba
        #print "fin cantidad"

        from datetime import date
        date = date.today()
        formaPago = form.vars.formaPago
        formaEntrega = form.vars.formaEntrega
        domiEntrega = form.vars.idDomicilio
        venta = db(db.venta.id == idVenta).select().first()
        venta.fechaPedido = date
        venta.formaPago = formaPago
        venta.formaEntrega = formaEntrega
        venta.idDomicilio = domiEntrega

        if formaEntrega == 'Entrega a domicilio':
            zonaDomicilio = db((db.zona.id == db.domicilio.idZona) & (db.domicilio.id == domiEntrega)).select().first()
            #print zonaDomicilio
            venta.costoEntrega = zonaDomicilio.zona.precio
            venta.importeTotal = importe + zonaDomicilio.zona.precio
            venta.estado = "Pendiente confirmar fecha"
        elif formaEntrega == 'Retira en local':
            venta.importeTotal = importe
            venta.estado = "Retira"
        else:
            venta.importeTotal = importe
            venta.estado = "Espera acuerdo"

        venta.update_record()
        #print venta
    except Exception as blumba:
        print blumba


def mostrarCompraRealizada():
    idVenta = request.args[0]
    # = db(db.venta.id == idVenta).select().first()
    detVenta = db((db.detalleVenta.idVenta == idVenta)&(db.producto.id==db.detalleVenta.idProducto)).select()
    importeTotal = 0
    for row in detVenta:
        importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

    formVenta = SQLFORM(db.venta,  idVenta, readonly=True)

    return locals()


#Listado del Usuario - podrá consultar #
def listadoCompras():

    form = SQLFORM.factory(
            Field('fechaDesde','date', label='Fecha desde:', default=None),
            Field('fechaHasta','date', label='Fecha hasta:', default=None),
            Field('estado','string', label='Estado:', default=None, requires=IS_EMPTY_OR(IS_IN_SET(["Pendiente", "Finalizado",
                                                                                                    "Pendiente confirmar fecha",
                                                                                                    "Delivery", "Retira", "Entregado"]))),
            submit_button='Buscar')

    if form.process().accepted:
        response.flash = None
        query = armarQueryCompra(form, auth.user.id)
        grid = SQLFORM.grid(query,
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('compra','mostrarCompraRealizada/%s'%row.id) ))])
    else:
        grid = SQLFORM.grid(((db.venta.idCliente == auth.user.id)&(db.venta.formaEntrega is not None)),
                            create = False,
                            deletable = False,
                            editable=False,
                            details=False,
                            searchable=False,
                            csv = False,
                            links_in_grid=True,
                            links = [dict(header=' ',body=lambda row: A('Ver detalle',_class="button btn btn-default",
                                                                        _href=URL('compra','mostrarCompraRealizada/%s'%row.id) ))])
    return locals()
