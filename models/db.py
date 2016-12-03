# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()


db.define_table(
    auth.settings.table_user_name,
    Field('dni','integer', required=True,  label=T('DNI')),
    Field('last_name', 'string',  length=128, required=True, label=T('Apellido')),
    Field('first_name', 'string', length=128,  required=True, label=T('Nombre')),
    Field('email', 'string',  length=128,   required=True, label=T('E-Mail')),
    Field('celular', 'string', length=20, label=T('Celular')),
    Field('password', 'password', length=512, required=True, readable=False, label='Contraseña'),
    Field('registration_key', length=512,
          writable=True, readable=False, label=T('Clave de registración')),
    Field('reset_password_key', length=512,
          writable=False, readable=False,label=T('Clave de contraseña de restablecimiento'))
          )
auth.settings.create_user_groups = False
# VALIDADORES DE LA TABLA DE USUARIOS
usuario = db[auth.settings.table_user_name] # Con esto se abrevia todo en 'usuario'
usuario.dni.requires=IS_NOT_EMPTY(error_message='Falta Ingresar DNI')
usuario.first_name.requires=IS_NOT_EMPTY(error_message='Falta ingresar Nombre')
usuario.last_name.requires=IS_NOT_EMPTY(error_message='Falta ingresar Apellido')
usuario.password.requires=IS_NOT_EMPTY(error_message='Falta ingresar Contraseña')
usuario.email.requires = [
  IS_EMAIL(error_message='El E-mail ingresado no es valido.Intente nuevamente.'),
  IS_NOT_IN_DB(db, usuario.email)]
auth.settings.register_next = URL('index', args='login')
#fin de validadores

mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False


# mail.settings.server =  'smtp.gmail.com:587'  # your SMTP server
# mail.settings.sender = 'villan.laura@gmail.com'         # your email
# mail.settings.login = 'villan.laura@gmail.com:klavier.ale.15185' # your credentials or None

auth.settings.hmac_key = 'sha512:d5a9296b-86d3-4ae3-bd4f-e19faa94d6e3'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False #TODO: quitar luego de terminar: True
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = False
#auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'
auth.messages.label_remember_me = 'Seguir conectado(por 30 días)' 

'''
# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

'''
#unique=True, bug https://groups.google.com/forum/#!topic/web2py/PLoVjDti-lE
#db.categoria.truncate()

#Categoria: vinos/accesorios/espumantes/
db.define_table('categoria',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    )
db.categoria.nombre.requires=[IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                              IS_NOT_IN_DB(db, 'categoria.nombre',error_message='Ya existe')]
db.categoria.id.label='Número'

#TipoVinos : blanco, oporto, rosado, dulces, tardio, tinto, etc.
db.define_table('tipoVino',
    Field('tipo', 'string',  required=True, notnull=True, label=T('Tipo de vino') ),
    )
db.tipoVino.tipo.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                             IS_NOT_IN_DB(db, 'tipoVino.tipo',error_message='Ya existe')]
db.tipoVino.id.label='Número'

#Varietal:malbec, syrah, tempranillo
db.define_table('varietal',
    Field('tipoVarietal', 'string', required=True, notnull=True, label=T('Varietal') ),
    )
db.varietal.tipoVarietal.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el varietal '),
                                     IS_NOT_IN_DB(db, 'varietal.tipoVarietal',error_message=' Ya existe ')]
db.varietal.id.label='Número'

#Bodega
db.define_table('bodega',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('descripcion', 'text', label=T('Descripción')),
    Field('web', 'string', label=T('Página Web')),
    )
db.bodega.nombre.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el nombre'),
                             IS_NOT_IN_DB(db, 'bodega.nombre',error_message='Ya existe')]
db.bodega.id.label='Número'
db.bodega.nombre.writable = True
db.bodega.descripcion.writable = True

#noticias
db.define_table('noticia',
    Field('titulo', 'string', required=True, notnull=True, label=T('Titulo') ),
    Field('copete', 'string', label=T('Copete')),
    Field('cuerpo', 'text', label=T('Cuerpo')),
    Field('autor', 'string', label=T('Autor')),
    Field('fecha', 'date', label=T('Fecha')),
    #Verificar como se guardan las imagenes
    Field('imagen', 'upload', label=T('Imagen'), autodelete=True),
    )
db.noticia.titulo.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el titulo'),
                              IS_NOT_IN_DB(db, 'noticia.titulo', error_message=' Ya existe ')]
db.noticia.id.label='Número'

#Eventos
db.define_table('evento',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('caracteristicas', 'text', label=T('Características')),
    Field('requisitos', 'text', label=T('Requisitos')),
    Field('fecha', 'date', label=T('Fecha')),
    Field('hora', 'time', label=T('Horario')),
    Field('duracion', 'decimal(2,2)', label=T('Duración')),
    )
db.evento.nombre.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el nombre'),
                             IS_NOT_IN_DB(db, 'evento.nombre', error_message=' Ya existe ')]
db.evento.duracion.requires = IS_DECIMAL_IN_RANGE(0,200)
db.evento.id.label='Número'


#Productos: vinos, copas, etc.
db.define_table('producto',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('categoria', 'reference categoria', required=True, notnull=True, label=T('Categoría') ),
    Field('tipo', 'reference tipoVino', label=T('Tipo') ),
    Field('varietal', 'reference varietal',  label=T('Varietal') ),
    Field('descripcion', 'text', label=T('Descripción') ),
    Field('origen', 'string',  label=T('Origen') ),
    Field('anio', 'string',  label=T('Año') ),
    Field('bodega', 'reference bodega',  label=T('Bodega') ),
    Field('cantidad', 'integer', label=T('Cantidad') ),
    Field('precioCompra', 'decimal(9,2)', label=T('Precio compra') ),
    Field('precioVenta', 'decimal(9,2)', label=T('Precio venta') ),
    Field('imagen', 'upload', label=T('Imagen'),autodelete=True),#, uploadfolder=os.path.join(request.folder,'static/temp') ),
    )
db.producto.nombre.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el nombre '),
                               IS_NOT_IN_DB(db, 'producto.nombre', error_message=' Ya existe ')]
db.producto.tipo.requires = IS_IN_DB(db,db.tipoVino.id, "%(tipo)s")
db.producto.categoria.requires = IS_IN_DB(db,db.categoria.id, "%(nombre)s")
db.producto.varietal.requires = IS_IN_DB(db,db.varietal.id, "%(varietal)s")
db.producto.bodega.requires = IS_IN_DB(db,db.bodega.id, "%(nombre)s")
db.producto.cantidad.requires = IS_INT_IN_RANGE(0, 1e100)
db.producto.precioCompra.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.precioVenta.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.id.label='Número'

#Promociones por compras en la página
db.define_table('promocion',
    Field('promo', 'string', required=True, notnull=True, label=T('Promoción') ),
    Field('descripcion', 'string', label=T('Descripción')),
    Field('letraChica', 'string', label=T('Lectra chica')),
    Field('fechaDesde', 'date', label=T('Fecha desde')),
    Field('fechaHasta', 'date', label=T('Fecha hasta')),
    )
db.promocion.promo.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar la promo'),
                              IS_NOT_IN_DB(db, 'promocion.promo', error_message=' Ya existe ')]
db.promocion.id.label='Número'
#db.promocion.fechaHasta.requires = IS_DATE_IN_RANGE(format=T('%d-%m-%y'), minimum=form.vars.fechaDesde if form.vars.fechaDesde else None,
#                                                    maximum=None,
#                                                    error_message='Debe ser mayor a %s' form.vars.fechaDesde.strftime('%d-%m-%Y') if form.vars.fechaDesde else 'Fecha desde es obligatoria'
########################################################################

