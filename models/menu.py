response.logo = A(IMG(_src=URL('static', 'images/BukinoLogo.jpg'), _href=URL('default', 'index'), _class="navbar-brand" ))
response.title = request.application.replace('_', 'Bukino').title()
response.subtitle = ''

response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
#if auth.has_membership(role="admin"):
    #response.menu.extend([(T('Admin?'), False, URL(c='appadmin'), [])])
response.menu = [
        (T('Catálogo'), False, '#', [
            (T('Accesorios'), False, URL('producto','productosListados/1') ),
            (T('Cristalería'), False, URL('producto','productosListados/2') ),
            (T('Cofres'), False, URL('producto','productosListados/6') ),
            (T('Espumantes'), False, URL('producto','productosListados/4') ),
            (T('Estuches'), False, URL('producto','productosListados/5') ),
            (T('Vinos'), False, URL('producto','productosListados/3') ),
            ]),
        (T('Contacto'), False, '#', [
            (T('Ver'), False, URL('contacto','agregar') ),
            (T('Admin'), False, URL('contacto','admin') ),
        ]),
        (T('Eventos'), False, '#', [
            (T('Ver'), False, URL('default','index') ),
            (T('Administrar eventos'), False, URL('evento','admin') ),
            ]),
        (T('Noticias'), False, '#', [
            (T('Ver'), False, URL('noticia','index') ),
            (T('Administrar'), False, URL('noticia','admin') ),
        ]),
        (T('Productos'), False, '#', [
            (T('Listado'), False, URL('producto','index') ),
            (T('Administrar productos'), False, URL('producto','admin') ),
        ]),
        (T('Promociones'), False, '#', [
            (T('Ver'), False, URL('promocion','index') ),
            (T('Administrar promociones'), False, URL('promocion','admin') ),
        ]),
        (T('Usuarios'), False, '#', [
            (T('Listado'), False, URL('usuario','index') ),
            (T('Administrar usuarios'), False, URL('usuario','administrarUsuarios') ),
        ]),
        (T('Administrar seleccionables'), False, '#', [
            (T('Bodega'), False, URL('abm', 'bodegaAbm')), LI(_class="divider"),
            (T('Categoria'), False, URL('abm', 'categoriaAbm')), LI(_class="divider"),
            (T('Formas de Pago'), False, URL('abm', 'formaPagoAbm')), LI(_class="divider"),
            (T('Tipo de Vino'), False, URL('abm', 'tipoVinoAbm')), LI(_class="divider"),
            (T('Varietal'), False, URL('abm', 'varietalAbm')), LI(_class="divider"),
            (T('Zonas de envío'), False, URL('abm', 'zonaAbm')), LI(_class="divider"),
        ]),
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('desarrollador'), False, '#', [
            #http://127.0.0.1:8000/admin/default/design/Vinoteca
            (T('Design'), False, URL('admin', 'default', 'design/%s' % app)), LI(_class="divider"),
            (T('Controller'), False, URL('admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
            (T('View'), False, URL('admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
            (T('DB Model'), False, URL('admin', 'default', 'edit/%s/models/db.py' % app)),
            (T('Menu Model'), False, URL('admin', 'default', 'edit/%s/models/menu.py' % app)),
            (T('Eliminar BD'), False, URL('desarrollador', 'admin')), LI(_class="divider"),

            ]),
            ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
