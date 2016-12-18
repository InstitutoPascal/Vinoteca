# -*- coding: utf-8 -*-
def impactarProducto():
#    try:
    producto = request.vars.idProducto
    cantidad = request.vars.cantidad
    categoria = request.vars.categoria
    if auth.user:
        if tieneVentaVigente(auth.user.id):
            #do update
            print 'tiene'
            ventaVigente = db((db.venta.idCliente == auth.user.id) & (db.venta.estado == 'Pendiente')).select(db.venta.id).first()
            resultadoDet = db.detalleVenta.insert(idVenta = ventaVigente, idProducto = producto, cantidad = cantidad)
            if resultadoDet != None:
                print 'insertó'
                response.flash = 'Artículo agregado al carrito de compra.'
            redirect(URL('producto', 'productosListados/%s'%categoria ))
        else:
            #do inserts venta- detalle
            print 'no tiene venta vigente'
            resultado = db.venta.insert(idCliente = auth.user.id, estado = 'Pendiente')
            print resultado
            if resultado  != None:
                resultadoDet = db.detalleVenta.insert(idVenta = resultado, idProducto = producto, cantidad = cantidad)
                if resultadoDet  != None:
                    print 'insertó'
                    response.flash = 'Artículo agregado al carrito de compra.'
                else:
                    response.flash = 'Falló al  agregarlo.'

                redirect(URL('producto', 'productosListados/%s'%categoria ))
            else:
                print 'fallo'
                response.flash = 'Intentó realizar una acción que requiere que se encuentre logueado.'
                redirect(URL('producto', 'productosListados/%s'%categoria ))


    else:
        print 'Fallo'
        response.flash = 'Intentó realizar una acción que requiere que se encuentre logueado.'
        redirect(URL('producto', 'productosListados/%s'%categoria ))


#    except Exception as blumba:
#        print blumba
    return locals()


def cancela():
    #print 'Paso - Cancela compra'
    idVenta = request.args[0]
    #print idVenta
    db(db.detalleVenta.idVenta== idVenta).delete()
    db(db.venta.id == idVenta).delete()
    redirect(URL('producto', 'productosListados/1' ))
    return locals()

def validateDomicilio(form):
    formaPago = form.vars.formaPago
    formaEntrega = form.vars.formaEntrega
    domiEntrega = form.vars.idDomicilio

    if formaEntrega == None:
        form.errors.formaEntrega = "Debe seleccionar una forma de entrega."
    if (formaEntrega == "Entrega a domicilio") and (domiEntrega == None):
        form.errors.idDomicilio = "Para *Entrega a domicilio* se requiere un domicilio."
    else:
        pass

def detalleVentaCliente():
    #print 'Detalle venta Cliente'
    idVenta = request.args[0]
    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
        cantDomicilio = db(db.domicilio.idCliente == auth.user.id).count()
        if (cantDomicilio != None)&(cantDomicilio > 0 ) :
            registro = db((db.venta.id == idVenta) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro != None:
                idVenta = registro.id
                #print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

                #print 'Importe Total:'+ str(importeTotal)
                #print 'Formulario cargar detalles de venta - cliente'

                consultaCombo = db.domicilio.idCliente == auth.user.id
                form  = SQLFORM.factory(
                    Field("formaPago", label=T('Forma de pago'), requires=IS_IN_DB(db,db.formaPago.id, '%(descripcion)s', zero='Seleccionar',error_message="Ingrese una forma de pago.")),
                    Field("formaEntrega", 'string',  label=T('Forma de entrega'), requires=IS_EMPTY_OR(IS_IN_SET(["Acordar con el vendedor","Entrega a domicilio"]))),
                    Field("idDomicilio", label=T('Domicilio'), requires=IS_EMPTY_OR(IS_IN_DB(db(consultaCombo), db.domicilio.id, '%(calle)s - %(numero)s - %(idZona)s'))),
                    submit_button='Confirmar Compra')

                form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('default','index'))
                if form.process(onvalidation=validateDomicilio).accepted:
                    impactarCompra(idVenta,importeTotal,form)
                    redirect(URL('venta', 'mostrarCompraRealizada/%s' %idVenta))
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

def impactarCompra(idVenta,importe,form):
    try:
        #print 'ingresa'
        productosVendidos = db(db.detalleVenta.idVenta == idVenta).select()
        #print productosVendidos
        for prodVendido in productosVendidos:
            #print prodVendido.idProducto
            producto = db(db.producto.id == prodVendido.idProducto).select().first()
            print "pasa a borrar"
            #print prodVendido.idProducto
            stock = producto.cantidad-prodVendido.cantidad
            #db(db.producto.id == prodVendido.idProducto).update(cantidad = stock)
            #descomentar la linea de arriba
        print "fin cantidad"

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
        #venta.estado = "Finalizado"
        #descomentar esta linea


        if formaEntrega == 'Entrega a domicilio':
            zonaDomicilio = db((db.zona.id == db.domicilio.idZona) & (db.domicilio.id == domiEntrega)).select().first()
            #print zonaDomicilio
            venta.costoEntrega = zonaDomicilio.zona.precio
            venta.importeTotal = importe + zonaDomicilio.zona.precio
        else:
            venta.importeTotal = importe
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
