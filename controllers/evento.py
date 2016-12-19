# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de promociones' )
    grid = SQLFORM.grid(db.promocion, deletable = False, editable=False, details=True, csv = False)
    return locals()

def admin():
    titulo = T(' Administración de eventos' )
    grid = SQLFORM.grid(db.evento, deletable = True, csv = False , editable=False, create=False, details=True, )
    agregar = A('Agregar evento', _href=URL('agregar'), _class='btn btn-default btn-large')
    return locals()

def agregar():
    titulo = T('Agregar evento')
    form = SQLFORM(db.evento)
    if form.process().accepted:
        session.flash = 'Registro insertado'
        envioMail('evento', form.vars.id)
        redirect(URL('evento','admin'))
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('admin'))

    return locals()

def listado():
    from datetime import datetime
    eventos = db(db.evento.fecha>datetime.today()).select()
    return locals()

def detalle():
    return locals()

def detalle():
    if len(request.args) > 0:
        eventoId = request.args[0]
        evento = db(db.evento.id==eventoId).select().first()
        volver = A('Volver',_href=URL('listado'),_class='btn btn-default')
    else:
        session.flash = 'No se ingreso una promo'
        redirect(request.env.http_referer)
    return locals()