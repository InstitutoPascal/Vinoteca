# -*- coding: utf-8 -*-
#obtiene los Labels de la bd y lo devuelve en formato de headers
def get_header_labels(table=None):
    headers = {}
    for field in db[table].fields:
        headers[table+'.'+field] = db[table][field].label
    headers[table+'.id']= 'Número'
    return headers

#transforma los titulos de los formularios genericos
def obtenerTitulo(titulo=None):
    if titulo =='tipoVino':
        titulo = 'tipo de vino'
    elif  titulo =='formaPago':
        titulo = 'Forma de Pago'
    elif  titulo =='zona':
        titulo = 'Zonas de Envío'
    else:
        pass
    return titulo

##############################################################################
################## Metodo utilizado en ABM.py ################################
def abm(tabla_req=None):
    try:
        response.view = "%s/%s.%s" % (request.controller, 'abm', request.extension)

        form=SQLFORM(db[tabla_req], submit_button='Enviar')
        if form.accepts(request.vars,session):
            response.flash='Registro ingresado exitosamente '
        elif form.errors:
            response.flash='Complete el formulario '
        else:
            pass
        t = obtenerTitulo(tabla_req)
        titulo = T(' Administración de %s' % t)
        headersT = get_header_labels(tabla_req)

        regs=db(db[tabla_req].id>0).select()
    except Exception, e:
        print 'Fallo: %s' % e
    return locals()

########################################################################################################################
########### recibe desde donde se invoca y el id del registro nuevo   ##################################################
def envioMail(tipoMail=None, id = None):
    try:
        ok = True
        if tipoMail == 'evento':
            mensaje = 'mailNovedadEvento.html'
            subject = 'No te pierdas el nuevo evento'
            tabla = 'evento'
        elif tipoMail == 'promocion':
            mensaje = 'mailNovedadPromo.html'
            subject = 'Gran PROMOCIÓN'
            tabla = 'promocion'
        elif tipoMail == 'noticia':
            mensaje = 'mailNovedadNoticia.html'
            subject = 'Novedades!'
            tabla = 'noticia'
        else:
            ok = False
        if ok:
            for usuario in db(db.auth_user.novedades == True).select():
                print 'Usuario: '+ usuario.last_name
                context = dict(usuario=usuario,informa=db(db[tabla]._id==id).select().first())
                mensaje = response.render(mensaje, context)
                mail.send(to=usuario.email,
                          subject=subject,
                          message=mensaje)
        else:
            print 'Llamaste a la funcion de envio de mail con una opcion no valida. chequealo antes dolobu'
    except Exception, e:
        print 'Fallo: %s' % e
    else:
        print 'sin problemas'
    finally:
        print 'listo'
    return None

###############################################################################################################
def getModal(id, titulo, mensaje, textoAccion):
    return '''
<div class="modal fade" id="%s" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">%s</h4>
            </div>
            <div class="modal-body">
                %s
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Cancelar</button>
                <a class="btn btn-danger btn-ok" data-dismiss="modal" >%s</a>
            </div>
        </div>
    </div>
</div>
    '''%(id,titulo,mensaje,textoAccion)

def setSuscripcion(suscribir):
    resultado = ''

    print 'suscribir: %s'%suscribir
    try:
        user_row = db(db.auth_user.id==auth.user.id).select().first()
        user_row.novedades = suscribir
        result = user_row.update_record()
        auth.user.novedades = suscribir
        auth.user.update()
        if result:
            resultado = T('Suscripcion correcta') if suscribir else T('Desuscripcion correcta')
        else:
            resultado = T('No se pudo suscribir') if suscribir else T('No se pudo desuscribir')
    except Exception as e:
        resultado = T('Ocurrio un error al acutalizar la suscripcion a novedades: ') + e
        print e
    return resultado


################# Ventas #######
def tituloCategoria(categoria):
    print categoria
    titulo = 'Catalogo de'
    if categoria == '1':
        titulo += ' accesorios '
    elif categoria == '2':
        titulo += ' cristalería '
    elif categoria == '3':
        titulo += ' vinos '
    elif categoria == '4':
        titulo += ' espumantes'
    elif categoria == '5':
        titulo += ' estuches '
    elif categoria == '6':
        titulo += ' cofres '
    else:
        titulo = ' El link ingresado no es correcto '
    return titulo

def armarQuery(form, categoria):
    try:
        query=None
        #print '1 - ' + form.vars.nombre
        #print '2 - ' + form.vars.precioMenor
        #print '3 - ' + form.vars.precioMayor

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

        query = isNoneConcat(query,(db.producto.categoria == categoria)&(db.producto.cantidad > 0))
        print query

    except Exception as blumba:
        print blumba
    return query

def isNoneConcat(resultado, consulta):
    if resultado is not None:
        resultado &=  consulta
    else:
        resultado = consulta
    return resultado


def tieneVentaVigente(user):
    try:
        tiene = False
        cantidad = db((db.venta.idCliente == user) & (db.venta.estado == 'Pendiente')).count()
        if  cantidad > 0:
            tiene = True

    except Exception as blumba:
        print blumba
    return tiene

# def enviarEmail(contexto, template, destino, mensaje = None, formatoFecha=None):
#     try:
#         if mensaje is not None:
#             contexto.mensaje = mensaje
#         message = response.render(template, contexto)
#         result = mail.send(to=destino, subject=motivo, message=message, headers=dict(contentType='text/html; charset="UTF-8"'))
#         if result:
#             print 'Email enviado'
#         else:
#             print 'No se pudo enviar el email'
#     except Exception as e:
#         print 'Ocurrio un error al enviar el email: %s '%e

######## lista de compras ###########################

def armarQueryCompra(form, idUser):
    try:
        query=None
        #print '1 - ' + str(form.vars.fechaDesde)
        #print '2 - ' + str(form.vars.fechaHasta)
        #print '3 - ' + str(form.vars.estado)
        if form.vars.estado is not None:
            query = (db.venta.estado.like('%'+str(form.vars.estado)+'%'))

        if form.vars.fechaDesde != '' and form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde) & (db.venta.fechaPedido <= form.vars.fechaHasta))
        elif form.vars.fechaDesde != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde))
        elif form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido <= form.vars.fechaHasta))
        else:
            pass

        query = isNoneConcat(query,(db.venta.idCliente == idUser) & (db.venta.formaEntrega is not None))
        #print query
    except Exception as blumba:
        print blumba
    return query


def armarQueryVentas(form):
    try:
        query=None

        if form.vars.cliente is not None:
            query = (db.venta.idCliente == form.vars.cliente)

        if form.vars.estado is not None:
            query = (db.venta.estado.like('%'+str(form.vars.estado)+'%'))

        if form.vars.fechaDesde != '' and form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde) & (db.venta.fechaPedido <= form.vars.fechaHasta))
        elif form.vars.fechaDesde != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde))
        elif form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido <= form.vars.fechaHasta))
        else:
            pass

        query = isNoneConcat(query, (db.venta.formaEntrega is not None) & (db.venta.estado != "Entregado"))
        #print query
    except Exception as blumba:
        print blumba
    return query


def armarQueryReporte(form):
    try:
        query=None

        if form.vars.cliente is not None:
            query = (db.venta.idCliente == form.vars.cliente)

        if form.vars.fechaDesde != '' and form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde) & (db.venta.fechaPedido <= form.vars.fechaHasta))
        elif form.vars.fechaDesde != '':
            query = isNoneConcat(query,(db.venta.fechaPedido >= form.vars.fechaDesde))
        elif form.vars.fechaHasta != '':
            query = isNoneConcat(query,(db.venta.fechaPedido <= form.vars.fechaHasta))
        else:
            pass

        query = isNoneConcat(query, (db.venta.estado == "Entregado"))
        #print query
    except Exception as blumba:
        print blumba
    return query
