# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de promociones' )
    grid = SQLFORM.grid(db.promocion, deletable = False, editable=False, details=True, csv = False)
    return locals()



def admin():
    titulo = T(' Administración de promociones' )
    grid = SQLFORM.grid(db.promocion, deletable = True, csv = False , editable=False, create=False, details=True, )
    agregar = A('Agregar promoción', _href=URL('agregar'), _class='btn btn-default btn-large')
    return locals()

def validateDates(form):
    fd = form.vars.fechaDesde
    fh = form.vars.fechaHasta
    if fd > fh:
        form.errors.fechaHasta = 'La fecha desde tiene que ser anterior a la fecha hasta'


def agregar():
    titulo = T('Agregar promoción')
    form = SQLFORM(db.promocion)
    if form.process(onvalidation=validateDates).accepted:
        session.flash = 'Registro insertado'
        envioMail('promocion', form.vars.id)
        redirect(URL('promocion','admin'))
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('admin'))
    #comento el boton que se supone que no hace nada mimodal=getModal('volverConfirmacion', 'Volver', '<p>Desea volver, perdera los cambios</p>','Volver')
    return locals()
