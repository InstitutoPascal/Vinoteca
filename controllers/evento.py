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
    if form.process(onvalidation=validateDates).accepted:
        session.flash = 'Registro insertado'
        envioMail('evento', form.vars.id)
        redirect(URL('evento','admin'))
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('admin'))

    return locals()
