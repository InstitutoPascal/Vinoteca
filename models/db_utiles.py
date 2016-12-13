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
    else:
       pass
    return titulo

##############################################################################
################## Metodo utilizado en ABM.py ################################
def abm(tabla_req=None):
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
        auth.user = user_row
        result = user_row.update_record()
        print auth.user.novedades
        print 'novedades auth:%s,record:%s'%(user_row.novedades,auth.user.novedades)
        if result:
            resultado = T('Suscripcion correcta') if suscribir else T('Desuscripcion correcta') 
        else:
            resultado = T('No se pudo suscribir') if suscribir else T('No se pudo desuscribir') 
    except Exception as e:
        resultado = T('Ocurrio un error al acutalizar la suscripcion a novedades: ') + e
        print e
    return resultado