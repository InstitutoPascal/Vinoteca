#@auth.requires_login()
def administrarUsuarios():
    grid = SQLFORM.grid(db.auth_user,
        create = False,
        deletable = False,
        editable=True,
        details=True,
        csv = True,
        exportclasses = dict(cvs = False,
            xml = False,
            csv_with_hidden_cols = False,
            tsv_with_hidden_cols = False,
            tsv = False,
            json = False )
    )
    return locals()

def subscribe():
    suscribir = len(request.args) == 0 or request.args[0]==str(True)
    setSuscripcion(suscribir)
    return True

@auth.requires_login()
def listarDirecciones():
    if auth.user:
        grid = SQLFORM.grid(
            db(db.domicilio.idCliente == auth.user.id), 
            create = False,
            deletable = True,
            editable=False,
            details=False,
            searchable=False,
            csv = False
        )
        agregar = A(T('Agregar'), _href=URL('agregarDireccion/%s'%auth.user.id), _class='btn btn-primary')
    return locals()

@auth.requires_login()
def agregarDireccion():
    if auth.user:
        form = SQLFORM.factory(
            Field("referencia", "string", required=True, notnull=True, label=T('Referencia del domicilio: '),
                requires=IS_NOT_EMPTY(error_message=T('Falta ingresar la referencia al domicilio'))
            ),
            Field("calle", "string", required=True, notnull=True,
                requires=IS_NOT_EMPTY(error_message=T('Falta ingresar la calle')) ,label=T('Calle: ')
            ),
            Field("numero", "integer", required=True, label=T('Nro: '),
                notnull=True, requires=IS_NOT_EMPTY(error_message=T('Falta ingresar la calle'))
            ),
            Field("piso", "string", label=T('Piso: ')),
            Field("departamento", "string", label=T('Depto: ')),
            Field("otros", "string", label=T('Otros ')),
            Field("idZona", "integer", required=True, notnull=True, label=T('Zona'),
                requires=IS_IN_DB(db, 'zona.id', ' %(descripcion)s', error_message=T('Falta ingresar la zona'))
            ),
        )
        if form.process().accepted:
            session.flash = T('Se ingreso una direccion con exito')
            form.vars.idCliente = auth.user.id
            id = db.domicilio.insert(**db.domicilio._filter_fields(form.vars))
            redirect(URL('listarDirecciones'))
        else:
            response.flash = T('ingrese los campos requeridos.')

    return locals()

def test():
    return FORM(INPUT(_name="test"))
