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
    print 'Paso a cancelar'
    idVenta = request.args[0]
    print idVenta
    db(db.detalleVenta.idVenta== idVenta).delete()
    db(db.venta.id == idVenta).delete()
    redirect(URL('producto', 'productosListados/1' ))
    return locals()

def detalleVentaCliente():
    print 'Paso a cancelar'
    idVenta = request.args[0]
    #Inicio -Verifica si tiene algo en el carrito#
    if auth.user:
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
        else:
            redirect(URL('default', 'index' ))

    else:
        redirect(URL('default', 'index' ))
    #FIN - Verifica si tiene algo en el carrito#
    return locals()
