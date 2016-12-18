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
    print formaPago
    print formaEntrega
    print domiEntrega
    if formaPago == 3 and (formaEntrega != None or domiEntrega != None):
        form.errors.formaPago = "Para *Entrega a domicilio* se requiere un domicilio."
    if (formaEntrega == "Entrega a domicilio") and (domiEntrega == None):
        form.errors.idDomicilio = "Para *Entrega a domicilio* se requiere un domicilio."
    else:
        pass

def detalleVentaCliente():
    print 'Detalle venta Cliente'
    idVenta = request.args[0]
    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
        cantDomicilio = db(db.domicilio.idCliente == auth.user.id).count()
        if (cantDomicilio != None)&(cantDomicilio > 0 ) :
            registro = db((db.venta.id == idVenta) & (db.venta.estado == 'Pendiente')).select().first()
            #print registro
            if registro != None:
                idVenta = registro.id
                print registro
                detVenta = db((db.detalleVenta.idVenta == registro.id)&(db.producto.id==db.detalleVenta.idProducto)).select()
                importeTotal = 0
                for row in detVenta:
                    importeTotal += (row.detalleVenta.cantidad * row.producto.precioVenta)

                #print 'Importe Total:'+ str(importeTotal)
                #print 'Formulario cargar detalles de venta - cliente'

                consultaCombo = db.domicilio.idCliente == auth.user.id
                form  = SQLFORM.factory(
                    Field("formaPago", label=T('Forma de pago'), requires=IS_IN_DB(db,db.formaPago.id, '%(descripcion)s', zero='Seleccionar')),
                    Field("formaEntrega", 'string',  label=T('Forma de entrega'), requires=IS_EMPTY_OR(IS_IN_SET(["Acordar con el vendedor","Entrega a domicilio"]))),
                    Field("idDomicilio", label=T('Domicilio'), requires=IS_EMPTY_OR(IS_IN_DB(db(consultaCombo), db.domicilio.id, '%(calle)s - %(numero)s - %(idZona)s'))),
                    submit_button='Confirmar Compra')

                form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('default','index'))
                if form.process(onvalidation=validateDomicilio).accepted:
                    response.flash = "Se envió pedido."
                    redirect(URL('default', 'index' ))
                else:
                    pass
            else:
                response.flash = "Falló al obtener la compra."
                redirect(URL('default', 'index' ))
        else:
            #Redirigir a administracion de Domicilio
            response.flash = "Debe cargar un domicilio antes de continuar con la compra."
            redirect(URL('usuario', 'listarDirecciones' ))
    else:
        response.flash = "Usuario no logueado."
        redirect(URL('default', 'index' ))
    #FIN - Verifica si tiene algo en el carrito#
    return locals()
