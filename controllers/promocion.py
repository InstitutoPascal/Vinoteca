# -*- coding: utf-8 -*-


def index():
    from datetime import date
    date = date.today()
    titulo = T(' Listado de promociones no vigentes' )
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
                        deletable = True,
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
    from datetime import date
    date = date.today()

    fd = form.vars.fechaDesde
    fh = form.vars.fechaHasta
    if fd < date:
        form.errors.fechaDesde = 'La fecha desde tiene que ser mayor al dia de hoy'

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
    return locals()


def listado():
    from datetime import datetime
    promociones = db(db.promocion.fechaDesde>datetime.today()).select()
    return locals()

def detalle():
    if len(request.args) > 0:
        promoId = request.args[0]
        promo = db(db.promocion.id==promoId).select().first()
        descripcion = XML(promo.descripcion, sanitize=True)
        producto = db(db.producto.id == promo.producto).select().first()
        if (promo.producto!=None):
            producto = producto.nombre
        varietal = db(db.varietal.id == promo.varietal).select().first()
        if (promo.varietal!=None):
            varietal = varietal.tipoVarietal
        volver = A('Volver',_href=URL('listado'),_class='btn btn-default')
    else:
        session.flash = 'No se ingreso una promo'
        redirect(request.env.http_referer)

    return locals()