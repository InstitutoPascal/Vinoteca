# -*- coding: utf-8 -*-

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', label=T('Nombre/s')),
    Field('last_name', label=T('Apellido/s')),
    Field('email', required=True, notnull=True, label=T('Correo Electrónico') ), # requerido
    Field('password', 'password', readable=False, label='Password'),
    Field('nacimiento','date', label=T('Fecha de Nacimiento')),
    Field('ciudad', 'string', label=T('Ciudad') ),
    Field('telefono', 'integer', label=T('Teléfono')),
    Field('fecha_alta', 'datetime', default=request.now, update=request.now, writable=False),
    Field('fecha_baja', 'datetime', writable=False, readable=False, default = None),
    Field('registration_key', length=512, writable=False, readable=False, default=''),#no quitar ni tocar
    Field('reset_password_key', length=512, writable=False, readable=False, default=''), #no quitar ni tocar
    Field('registration_id', length=512, writable=False, readable=False, default=''), #no quitar ni tocar
    Field('novedades', 'boolean', default=True, label=T('¿Desea recibir novedades y eventos de la página?') ),
    format = '%(first_name)s - %(last_name)s'
)


auth_table_especial = db[auth.settings.table_user_name]
auth_table_especial.first_name.requires =   IS_NOT_EMPTY(error_message = auth.messages.is_empty)
auth_table_especial.last_name.requires =   IS_NOT_EMPTY(error_message = auth.messages.is_empty)
auth_table_especial.password.requires = [IS_STRONG(error_message = 'La longitud mínima es 8 caracteres. Debe incluir al menos 1 minúscula, 1 mayúscula, 1 número y un simbolo. Ej: Pepe!001'), CRYPT()]
auth_table_especial.nacimiento.requires = IS_DATE(error_message = 'Debe ingresar una fecha')
auth_table_especial.email.requires = [IS_EMAIL(error_message = auth.messages.invalid_email),
                                      IS_NOT_IN_DB(db, auth_table_especial.email)]
auth_table_especial.nacimiento.represent = lambda v, r: '' if v is None else v
auth_table_especial.ciudad.represent = lambda v, r: '' if v is None else v
auth_table_especial.telefono.represent = lambda v, r: '' if v is None else v
auth.settings.table_user = auth_table_especial
# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)
auth.settings.create_user_groups = False
auth.settings.everybody_group_id = 3 # = autuevo seteo grupo: ('Usuarios(3)')
auth.settings.password_min_length = 6
# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging'#myconf.get('smtp.server')#
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False


def usuarioBaneado(form):
    reg = db(db.auth_user.email == form.vars.email).select(db.auth_user.fecha_baja).first()
    if reg !=None and reg.fecha_baja <> None:
        form.errors.email = 'El usuario está dado de baja por el administrador'



auth.settings.login_onvalidation = usuarioBaneado

# auth.settings.on_failed_authentication=` form
# auth.settings.login_url = URL('default','login')



# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.messages.verify_email = 'Haz clic en el link http://' + \
    request.env.http_host + \
    URL(r=request,c='default',f='user',args=['verify_email']) + \
    '/%(key)s para verificar tu dirección de correo electrónico'
auth.messages.reset_password = 'Haz clic en el link http://' + \
    request.env.http_host + \
    URL(r=request,c='default',f='user',args=['reset_password']) + \
    '/%(key)s para restablecer tu contraseña'


#Para deshabilitar una acción agrega su nombre a la siguiente lista:
#auth.settings.actions_disabled = []
#Por ejemplo=  auth.settings.actions_disabled.append('register')

#auth.settings.formstyle = 'table3cols' (puede ser "table2cols", "divs" y "ul")

auth.messages.submit_button = 'Enviar'
auth.messages.verify_password = 'Verificar contraseña'
auth.messages.delete_label = 'Marque para eliminar:'
auth.messages.function_disabled = 'Función deshabilitada'
auth.messages.access_denied = 'Acceso denegado'
auth.messages.registration_verifying = 'El registro de usuario requiere verificación'
auth.messages.login_disabled = 'El acceso fue deshabilitado por el administrador'
auth.messages.logged_in = 'Inicio de sesión'
auth.messages.email_sent = 'Correo enviado'
auth.messages.unable_to_send_email = 'Falló el envío del correo'
auth.messages.email_verified = 'Dirección de correo verificada'
auth.messages.logged_out = 'Se ha cerrado la sesión'
auth.messages.registration_successful = 'Registro de usuario completado'
auth.messages.invalid_email = 'Dirección de correo inválida'
auth.messages.unable_send_email = 'Falló el envío del correo'
auth.messages.invalid_login = 'Falló la autenticación'
auth.messages.invalid_user = 'El usuario especificado no es válido'
auth.messages.is_empty = "No puede ser vacío"
auth.messages.mismatched_password = "Los campos de contraseña no coinciden"
#auth.messages.verify_email = "Verifique su casilla de correo electrónico"
auth.messages.verify_email_subject = 'Verificación de contraseña'
auth.messages.new_password_sent = 'Se ha enviado una nueva contraseña a su correo'
auth.messages.password_changed = 'Contraseña modificada'
auth.messages.retrieve_password = 'Su contraseña de usuario es: %(password)s'
auth.messages.retrieve_password_subject = 'Recuperar contraseña'
#auth.messages.reset_password = "Verifique su casilla de correo electrónico"
auth.messages.reset_password_subject = 'Restablecer contraseña'
auth.messages.invalid_reset_password = 'Nueva contraseña inválida'
auth.messages.profile_updated = 'Perfil actualizado'
auth.messages.new_password = 'Nueva contraseña'
auth.messages.old_password = 'Vieja contraseña'
auth.messages.group_description =  'Grupo exclusivo del usuario %(id)s'
auth.messages.register_log = 'Usuario %(id)s registrado'
auth.messages.login_log = 'Usuario %(id)s autenticado'
auth.messages.logout_log = 'Usuario %(id)s cerró la sesión'
auth.messages.profile_log = 'Usuario %(id)s perfil actualizado'
auth.messages.verify_email_log = 'Usuario %(id)s correo de verificación enviado'
auth.messages.retrieve_password_log = 'Usuario %(id)s contraseña recuperada'
auth.messages.reset_password_log = 'Usuario %(id)s contraseña restablecida'
auth.messages.change_password_log = 'Usuario %(id)s se cambió la contraseña'
auth.messages.add_group_log = 'Grupo %(group_id)s creado'
auth.messages.del_group_log = 'Grupo %(group_id)s eliminado'

auth.messages.label_remember_me = "Recordarme (por 30 días)"
