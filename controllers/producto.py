# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de productos sin stock' )
    grid = SQLFORM.grid(db(db.producto.cantidad == 0),
                        create = False,
                        deletable = True,
                        editable=True,
                        details=True,
                        csv = True,
                        exportclasses = dict(cvs = False,
                                             xml = False,
                                             csv_with_hidden_cols = False,
                                             tsv_with_hidden_cols = False,
                                             tsv = False,
                                             json = False )
                       )
    return locals()




def admin():
    titulo = T(' Administración de productos' )
    grid = SQLFORM.grid(db.producto, deletable = False, csv = True,exportclasses = dict(cvs = False,
                                                                                        xml = False,
                                                                                        csv_with_hidden_cols = False,
                                                                                        tsv_with_hidden_cols = False,
                                                                                        tsv = False,
                                                                                        json = False ))
    return locals()
