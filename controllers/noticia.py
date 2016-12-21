# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de noticias' )
    grid = SQLFORM.grid(db.noticia, deletable = False, editable=False, details=True, csv = False)
    return locals()

def oncreateNoticia(form):
    #print form.vars
    envioMail('noticia', form.vars.id)
    return True

def admin():
    titulo = T(' Administración de noticias' )
    grid = SQLFORM.grid(db.noticia, deletable = False, csv = True,  user_signature = False, oncreate=lambda form: oncreateNoticia(form) )
    return locals()


def listado():
    from datetime import datetime
    noticias = db(db.noticia).select(orderby=~db.noticia.fecha)
    return locals()

def detalle():
    if len(request.args) > 0:
        noticiaId = request.args[0]
        noticia = db(db.noticia.id==noticiaId).select().first()
        volver = A('Volver',_href=URL('listado'),_class='btn btn-default')
    else:
        session.flash = 'No se ingreso una promo'
        redirect(request.env.http_referer)
    return locals()
