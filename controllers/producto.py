# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de productos sin stock' )
    #consulta = db.producto.cantidad == 0
    #grid = crud.select(db.producto, consulta)
    grid = SQLFORM.grid(db(db.producto.cantidad > 0), 
                        deletable = False,
                        editable=True,
                        details=True,
                        csv = True,
                        exportclasses = dict(cvs = False, xml = False, csv_with_hidden_cols = False, tsv_with_hidden_cols = False,tsv = False )
                       )
    return locals()




def admin():
    titulo = T(' Administración de productos' )
    grid = SQLFORM.grid(db.producto, deletable = False, csv = True)
    return locals()
