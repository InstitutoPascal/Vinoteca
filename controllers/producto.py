# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de productos' )
    grid = SQLFORM.grid(db.producto, deletable = False, editable=False, details=True, csv = False)
    return locals()



def admin():
    titulo = T(' Administración de productos' )
    grid = SQLFORM.grid(db.producto, deletable = False, csv = True)
    return locals()
