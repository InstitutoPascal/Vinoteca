# -*- coding: utf-8 -*-


def index():
    from datetime import date
    date = date.today()
    titulo = T(' Listado de promociones' )
    grid = SQLFORM.grid(db.promocion.fechaHasta<date,
                        deletable = True,
                        searchable=False,
                        create=False,
                        editable=False,
                        details=True,
                        csv = False,
                        paginate=15)
    return locals()

def editar():
    titulo = T(' Administración de promociones' )
    grid = SQLFORM.grid(db.promocion, deletable = True, csv = False , editable=False, create=False, details=True )
    agregar = A('Agregar promocion', _href=URL('agregar'), _class='btn btn-default btn-large')
    editar = A('Agregar promocion', _href=URL('agregar','editar'), _class='btn btn-default btn-large')
    return locals()
    

def admin():
    titulo = T(' Administración de promociones' )
    grid = SQLFORM.grid(db.promocion,
                        deletable = False,
                        editable=True,
                        create=False,
                        details=True,
                        csv = True,
                        paginate=15,
                        exportclasses = dict(cvs = False,
                                             xml = False,
                                             csv_with_hidden_cols = False,
                                             tsv_with_hidden_cols = False,
                                             tsv = False,
                                             json = False))
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
