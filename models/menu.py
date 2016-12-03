# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
        (T('Catálogo'), False, '#', [
            (T('Ver'), False, URL('default','index') ),
            ]),
        (T('Eventos'), False, '#', [
            (T('Ver'), False, URL('default','index') ),
            ]),
        (T('Promociones'), False, '#', [
            (T('Ver'), False, URL('default','index') ),
        ]),
        (T('Noticias'), False, '#', [
            (T('Ver'), False, URL('noticia','index') ),
            (T('Administrar'), False, URL('noticia','admin') ),
        ]),
        (T('Contacto'), False, '#', [
            (T('Ver'), False, URL('default','index') ),
        ]),
        (T('Productos'), False, '#', [
            (T('Listado'), False, URL('producto','index') ),
            (T('Administrar productos'), False, URL('producto','admin') ),
        ]),
        (T('Administrar'), False, '#', [
            (T('Bodega'), False, URL('abm', 'bodegaAbm')), LI(_class="divider"),
            (T('Categoria'), False, URL('abm', 'categoriaAbm')), LI(_class="divider"),
            (T('Evento'), False, URL('abm', 'eventoAbm')), LI(_class="divider"),
            (T('Formas de Pago'), False, URL('abm', 'formaPagoAbm')), LI(_class="divider"),
            (T('Promocion'), False, URL('abm', 'promocionAbm')), LI(_class="divider"),
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
