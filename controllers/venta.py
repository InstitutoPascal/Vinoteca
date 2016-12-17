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


        #session.flash = 'Paso'

        #redirect(URL('producto', 'productosListados/%s'%categoria ))
#    except Exception as blumba:
#        print blumba
    return locals()


def cancela():
    print 'Paso - Cancela compra'
    idVenta = request.args[0]
    print idVenta
    db(db.detalleVenta.idVenta== idVenta).delete()
    db(db.venta.id == idVenta).delete()
    redirect(URL('producto', 'productosListados/1' ))
    return locals()

def detalleVentaCliente():
    print 'Detalle venta Cliente'
    idVenta = request.args[0]
    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
        cantDomicilio = db(db.domicilio.idCliente == auth.user.id).count()
        print cantDomicilio
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

                print 'Importe Total:'+ str(importeTotal)
                print 'Formulario cargar detalles de venta - cliente'
#                subset=db(db.person.id>100)
#                db.dog.owner.requires = IS_IN_DB(db, 'person.id', '%(name)s',
#                                                 _and=IS_NOT_IN_DB(subset,'person.id'))
                consultaCombo = db.domicilio.idCliente == auth.user.id
                form  = SQLFORM.factory(
                    Field("formaPago", label=T('Forma de pago'), requires=IS_IN_DB(db,db.formaPago.id, '%(descripcion)s', zero='Seleccionar')),
                    Field("formaEntrega", 'string',  label=T('Forma de entrega'), requires=IS_IN_SET(["Acordar con el vendedor","Entrega a domicilio"])),
                    Field("idDomicilio", label=T('Domicilio'), requires=IS_EMPTY_OR(IS_IN_DB(db(consultaCombo), db.domicilio.id, '%(calle)s - %(numero)s - %(idZona)s'))),
                    Field("costoEntrega", 'integer',  label=T('Costo de entrega') ),
                    Field("importeTotal","string", label=T('Importe Total') ),
                    submit_button='Confirmar Compra')


                if form.process().accepted:
                    response.flash = "Se envió pedido."
                else:
                    pass
            else:
                response.flash = "Falló al obtener la compra."
                redirect(URL('default', 'index' ))
        else:
            #Redirigir a administracion de Domicilio
            response.flash = "Debe cargar un domicilio antes de continuar con la compra."
            redirect(URL('default', 'index' ))
    else:
        response.flash = "Usuario no logueado."
        redirect(URL('default', 'index' ))
    #FIN - Verifica si tiene algo en el carrito#
    return locals()
