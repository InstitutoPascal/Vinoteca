# -*- coding: utf-8 -*-


def index():
    return locals()

def agregar():
    '''TODO: luego agregar los datos de contacto es un fromularion con consultas
    Bukino Vinoteca
    Tel: 011-4951-2236
    Cel:15-4787-7909
    '''
    titulo = 'Consultas o sugerencias'
    if auth.user:
        form = SQLFORM(contacto)
        form.vars.nombre = auth.user.first_name
        form.vars.apellido = auth.user.last_name
        form.vars.telefono = auth.user.telefono
        form.vars.email = auth.user.email
        pass
    else:
        form = SQLFORM(contacto)
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('default','index'))
    if form.process().accepted:
        aceptacionConsulta(form)
        redirect(URL('default','index'))
    return locals()

#@auth.requires_login()
def admin():
    rows = db((contacto.id > 0)& ~(contacto.estado==True)).select()
    titulo = 'Consultas o sugerencias'
    return locals()

def responder():
    datos = contacto[request.args[0]]
    form = FORM(
                TEXTAREA(_name='respuesta', _class='col-md-offset-3 col-md-3'),
                INPUT(_value='Enviar respuesta',_type='submit', _class='btn btn-primary bloque')) # ,,
    if form.accepts(request,session):
        datos.respuesta = form.vars.respuesta
        datos.estado = True
        datos.update_record()
        respuestaConsulta(datos)
        redirect(URL('contacto','admin'))
    #     exito = True
    # else:
    #     pass
    return locals()


def aceptacionConsulta(form):
    from datetime import date
    date = date.today()
    try:
        context = dict()
        context['nombre'] = form.vars.nombre
        context['consultaSugerencia'] = "consulta"
        context['fecha'] = date.strftime("%d/%m/%y")

        message = response.render('contacto/emailAceptacionConsulta.html', context)

        result = mail.send(to=form.vars.email, subject='Gracias por su consulta', message=message, headers=dict(contentType='text/html; charset="UTF-8"'))
        if result:
            print 'se envio'
        else:
            print 'no se envio'
    except Exception as e:
        print e

def respuestaConsulta(datos):
    from datetime import date
    date = date.today()
    try:
        context = dict(datos = datos, fecha = datos.fecha.strftime("%d/%m/%y"))

        message = response.render('contacto/emailRespuestaConsulta.html', context)

        result = mail.send(to=datos.email, subject='Gracias por su consulta', message=message, headers=dict(contentType='text/html; charset="UTF-8"'))
        if result:
            print 'se envio'
        else:
            print 'no se envio'
    except Exception as e:
        print e
#enviarEmail(context,'contacto/emailRespuestaConsulta.html',destino=datos.email)