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
    try:

        print 'Paso a cancelar'
        idVenta = request.args[0]
        db(db.detalleVenta.id == idVenta).delete()
        db(db.venta.id == idVenta).delete()
    except Exception as blumba:
        print blumba
        redirect(URL('producto', 'productosListados/1' ))
    return locals()
