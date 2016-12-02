# -*- coding: utf-8 -*-

def abmCategoria():

    regs=db(db.categoria.id>0).select()

    form=SQLFORM(db.categoria)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = ''

    return {'form':form,'regs':regs}
