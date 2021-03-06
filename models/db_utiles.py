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
            i=0
            for usuario in db(db.auth_user.novedades == True).select():#TODO descomentar
                if i==0:
                    print 'Usuario: '+ usuario.last_name
                    context = dict(usuario=usuario, informa=db(db[tabla]._id==id).select().first())
                    mensaje = response.render(mensaje, context)
                    print mensaje
                    mail.send(to="villan.laura@gmail.com", #usuario.email,
                              subject=subject,
                              message=mensaje)
                    i+=1
                else:
                    pass
        else:
            print 'Llamaste a la funcion de envio de mail con una opcion no valida. chequealo antes dolobu'
    except Exception, e:
        print 'Fallo: %s' % e
    else:
        print 'sin problemas'
    finally:
        print 'listo'


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


def event_ins(nom,car,req,det,fe,fin,hora,dura,dir):
    db.evento.insert(
		nombre='%s'%nom,
	    caracteristicas='%s'%car,
	    requisitos='%s'%req,
	    detalle='%s'%det,
	    fecha='%s'%fe,
	    fecha_fin='%s'%fin,
	    hora='%s'%hora,
	    duracion='%s'%dura,
	    direccion='%s'%dir
    )
    return True

def noti_ins(tit,cop,cue,aut,fec,fold,ima):
    db.noticia.insert(
        titulo='%s'%tit,
        copete='%s'%cop,
        cuerpo='%s'%cue,
        autor='%s'%aut,
        fecha='%s'%fec,
        imagen=open('%s\%s'%(fold,ima), 'rb')
    )
    return True

def prom_ins(pro,por,des,let,dde,has,prd,var):
    db.promocion.insert(
        promo='%s'%pro,
        porcentaje='%s'%por,
        descripcion='%s'%des,
        letraChica='%s'%let,
        fechaDesde='%s'%dde,
        fechaHasta='%s'%has,
        producto='%s'%prd,
        varietal='%s'%var
    )
    return True
