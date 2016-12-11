# -*- coding: utf-8 -*-
# intente algo como


def index():
    '''TODO: luego agregar los datos de contacto es un fromularion con consultas
    Bukino Vinoteca
    Tel: 011-4951-2236
    Cel:15-4787-7909
    '''
    titulo = 'Consultas o sugerencias'
    form = SQLFORM(contacto)
    if form.process().accepted:
        sendMail(form)
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('default','index'))
    return locals()

#@auth.requires_login()
def admin():
    contacto.id.readable=False
    grid = SQLFORM.grid(contacto, editable=False, deletable=False, create=False, csv=False)
    titulo = 'Consultas o sugerencias'
    return locals()

def sendMail(form):
    try:
        context = dict()
        context['nombre'] = form.vars.nombre
        context['consultaSugerencia'] = "consulta"
        context['fecha'] = form.vars.fecha
        
        message = response.render('contacto/emailTemplate.html', context)

        result = mail.send(to=form.vars.email, subject='Gracias por su consulta', message=message, headers=dict(contentType='text/html; charset="UTF-8"'))
        if result:
            print 'se envio'
        else:
            print 'no se envio'
    except Exception as e:
        print e