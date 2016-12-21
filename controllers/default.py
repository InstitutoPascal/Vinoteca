# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    row,max = getMax('producto',db.producto.categoria == 3)
    productos = [
        row,
        getMax('producto',db.producto.categoria == 6)[0],
        getMax('producto',db.producto.categoria == 4)[0],
        getMax('producto',db.producto.categoria == 1)[0]
    ]
    row,max=getMax('producto',(db.producto.categoria == 3)&(db.producto.id<max))
    productos2 = [
        row,
        getMax('producto',(db.producto.categoria == 3)&(db.producto.id<max))[0],
        getMax('producto',(db.producto.categoria == 5))[0],
        getMax('producto',(db.producto.categoria == 2))[0]
    ]
    # evento = getMax('evento').row
    # promo = getMax('promocion').row
    # noticia = getMax('noticia').row

    if auth.user:
        dir = db(db.domicilio.idCliente == auth.user.id).select().first()
        if dir is None:
            response.flash = 'Recuerde que para realizar el pedido online deberá cargar un domicilio'
            
    return locals()

def getMax(tabla, query=None):
    max = db[tabla].id.max()
    maxid = db(query).select(max).first()[max]
    row = db[tabla][maxid]
    return [row,maxid]

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
