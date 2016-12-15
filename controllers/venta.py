# -*- coding: utf-8 -*-
def impactarProducto():
    try:
        print 'llegó'
        print request.vars.idProducto
        print request.vars.cantidad
        print request.vars.categoria
        producto = request.vars.idProducto
        cantidad = request.vars.cantidad
        categoria = request.vars.categoria
        if auth.user:
            if tieneVentaVigente(auth.user.id):
                #do update
                print 'tiene'
            else:
                #do inserts venta- detalle
                print 'no tiene venta vigente'
                resultado = insertarVentaYDetalle(auth.user.id, producto, cantidad)
                print resultado
        else:
            redirect(URL('producto', 'productosListados/%s'%categoria ))
            response.flash = 'Intentó realizar una acción que requiere que se encuentre logueado.'

        session.flash = 'Paso'

        redirect(URL('producto', 'productosListados/%s'%categoria ))
    except Exception as blumba:
        print blumba
    return locals()


def insertarVentaYDetalle(user, producto, cantidad):
    try:
        estado = False
        mensaje = ''
        
        #TODO continuar esto. en test.py estaba haciendo una prueba
        
    except Exception as blumba:
        print blumba
    return estado
