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

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)
auth.settings.create_user_groups = False
auth.settings.everybody_group_id = 3
auth.settings.password_min_length = 6
#auth.add_membership('Usuarios')
# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging'#myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

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
auth.messages.verify_email = ...
auth.messages.verify_email_subject = 'Verificación de contraseña'
auth.messages.new_password_sent = 'Se ha enviado una nueva contraseña a su correo'
auth.messages.password_changed = 'Contraseña modificada'
auth.messages.retrieve_password = 'Su contraseña de usuario es: %(password)s'
auth.messages.retrieve_password_subject = 'Recuperar contraseña'
auth.messages.reset_password = ...
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
auth.messages.add_membership_log = None
auth.messages.del_membership_log = None
auth.messages.has_membership_log = None
auth.messages.add_permission_log = None
auth.messages.del_permission_log = None
auth.messages.has_permission_log = None
auth.messages.label_first_name = 'Nombre'
auth.messages.label_last_name = 'Apellido'
auth.messages.label_email = 'Correo Electrónico'
auth.messages.label_password = 'Contraseña'
auth.messages.label_registration_key = 'Clave de registro de usuario'
auth.messages.label_reset_password_key = 'Clave para restablecer contraseña'
auth.messages.label_registration_id = 'Identificador del registro de usuario'
auth.messages.label_role = 'Rol'
auth.messages.label_description = 'Descripción'
auth.messages.label_user_id = 'ID del Usuario'
auth.messages.label_group_id = 'ID del Grupo'
auth.messages.label_name = 'Nombre'
auth.messages.label_table_name = 'Nombre de Tabla'
auth.messages.label_record_id = 'ID del Registro'
auth.messages.label_time_stamp = 'Fecha y Hora'
auth.messages.label_client_ip = 'IP del Cliente'
auth.messages.label_origin = 'Origen'
auth.messages.label_remember_me = "Recordarme (por 30 días)"
