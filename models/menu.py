response.logo = A(IMG(_src=URL('static', 'images/BukinoLogo.jpg'), _href=URL('default', 'index'), _class="navbar-brand" ))
response.title = request.application.replace('_', 'Bukino').title()
response.subtitle = ''

response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None
app = request.application
ctr = request.controller
# ----------------------------------------------------------------------------------------------------------------------
if auth.has_membership(role="Administrador"):
    response.menu = [
            (T('Catálogo'), False, '#', [
                (T('Accesorios'), False, URL('producto','productosListados/1') ),
                (T('Cristalería'), False, URL('producto','productosListados/2') ),
                (T('Cofres'), False, URL('producto','productosListados/6') ),
                (T('Espumantes'), False, URL('producto','productosListados/4') ),
                (T('Estuches'), False, URL('producto','productosListados/5') ),
                (T('Vinos'), False, URL('producto','productosListados/3') ),
                ]),
            (T('Consultas'), False, '#', [
                (T('Administrar consultas'), False, URL('contacto','admin') ),
                (T('Consultas o sugerencias'), False, URL('contacto','agregar') ),
            ]),
            (T('Eventos'), False, '#', [
                (T('Administrar eventos'), False, URL('evento','admin') ),
                (T('Ver'), False, URL('evento','listado') ),
                ]),
            (T('Noticias'), False, '#', [
                (T('Administrar noticias'), False, URL('noticia','admin') ),
                (T('Ver'), False, URL('noticia','listado') ),
            ]),
            (T('Productos'), False, '#', [
                (T('Administrar productos'), False, URL('producto','admin') ),
                (T('Listado productos faltantes'), False, URL('producto','index') ),
            ]),
            (T('Promociones'), False, '#', [
                (T('Administrar promociones'), False, URL('promocion','admin') ),
                (T('No vigentes'), False, URL('promocion','index') ),
                (T('Listado'), False, URL('promocion','listado') ),
            ]),
            (T('Usuarios'), False, '#', [
                (T('Baja usuario'), False, URL('usuario','bajaAltaUsuario') ),
                (T('Listado de usuarios'), False, URL('usuario','administrarUsuarios') ),
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
elif auth.has_membership(role="Usuario"):
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
                (T('Consultas o sugerencias'), False, URL('contacto','agregar') ),
            ]),
            (T('Eventos'), False, '#', [
                (T('Ver'), False, URL('evento','listado') ),
                ]),
            (T('Noticias'), False, '#', [
                (T('Ver'), False, URL('noticia','listado') ),
            ]),
            (T('Promociones'), False, '#', [
                (T('Ver'), False, URL('promocion','listado') ),
            ]),
    ]

elif auth.has_membership(role="Desarrollador"):
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
                (T('Administrar'), False, URL('contacto','admin') ),
                (T('Consultas o Sugerencias'), False, URL('contacto','agregar') ),
            ]),
            (T('Eventos'), False, '#', [
                (T('Administrar eventos'), False, URL('evento','admin') ),
                (T('Ver'), False, URL('default','index') ),
                (T('Listado'), False, URL('evento','listado') ),
                ]),
            (T('Noticias'), False, '#', [
                (T('Administrar noticias'), False, URL('noticia','admin') ),
                (T('Ver'), False, URL('noticia','index') ),
                (T('Listado'), False, URL('noticia','listado') ),
            ]),
            (T('Productos'), False, '#', [
                (T('Administrar productos'), False, URL('producto','admin') ),
                (T('Listado productos faltantes'), False, URL('producto','index') ),
            ]),
            (T('Promociones'), False, '#', [
                (T('Administrar promociones'), False, URL('promocion','admin') ),
                (T('Ver'), False, URL('promocion','index') ),
                (T('listado'), False, URL('promocion','listado') ),
            ]),
            (T('Usuarios'), False, '#', [
                (T('Baja usuario'), False, URL('usuario','bajaAltaUsuario') ),
                (T('Listado de usuarios'), False, URL('usuario','administrarUsuarios') ),
            ]),
            (T('Seleccionables'), False, '#', [
                (T('Bodega'), False, URL('abm', 'bodegaAbm')), LI(_class="divider"),
                (T('Categoria'), False, URL('abm', 'categoriaAbm')), LI(_class="divider"),
                (T('Formas de Pago'), False, URL('abm', 'formaPagoAbm')), LI(_class="divider"),
                (T('Tipo de Vino'), False, URL('abm', 'tipoVinoAbm')), LI(_class="divider"),
                (T('Varietal'), False, URL('abm', 'varietalAbm')), LI(_class="divider"),
                (T('Zonas de envío'), False, URL('abm', 'zonaAbm')), LI(_class="divider"),
            ]),
            (T('Utiles'), False, '#', [
            #http://127.0.0.1:8000/admin/default/design/Vinoteca
                (T('Design'), False, URL('admin', 'default', 'design/%s' % app)), LI(_class="divider"),
                (T('Controller'), False, URL('admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
                (T('View'), False, URL('admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
                (T('DB Model'), False, URL('admin', 'default', 'edit/%s/models/db.py' % app)),
                (T('Menu Model'), False, URL('admin', 'default', 'edit/%s/models/menu.py' % app)),
                (T('Admin'), False, URL('desarrollador', 'admin')), LI(_class="divider"),
            ]),

    ]

else:
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
                (T('Consultas o sugerencias'), False, URL('contacto','agregar') ),
            ]),
            (T('Eventos'), False, '#', [
                (T('Ver'), False, URL('evento','listado') ),
                ]),
            (T('Promociones'), False, '#', [
                (T('Ver'), False, URL('promocion','listado') ),
                ]),
            (T('Noticias'), False, '#', [
                (T('Ver'), False, URL('noticia','listado') ),
            ]),
            (T('Promociones'), False, '#', [
                (T('Ver'), False, URL('promocion','index') ),
                ]),
    ]

DEVELOPMENT_MENU = False


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
