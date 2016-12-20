# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    vino = db(db.producto.categoria == 3).select(orderby=db.producto.id).last()
    cofre = db(db.producto.categoria == 6).select(orderby=db.producto.id).last()
    espumante = db(db.producto.categoria == 4).select(orderby=db.producto.id).last()
    accesorio = db(db.producto.categoria == 1).select(orderby=db.producto.id).last()

    evento = db(db.evento.id > 0).select(orderby=db.evento.id).last()
    promo = db(db.promocion.id > 0 ).select(orderby=db.promocion.id).last()
    noticia = db(db.noticia.id > 0).select(orderby=db.noticia.id).last()
    aviso = None
    if auth.user:
        dir = db(db.domicilio.idCliente == auth.user.id).select().first()
        if dir is None:
            aviso = 'Recuerde que para realizar el pedido online deberá cargar un domicilio'

    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    return locals()#dict(message=T('Bukino'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
