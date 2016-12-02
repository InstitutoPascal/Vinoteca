# -*- coding: utf-8 -*-
#obtiene los Labels de la bd y lo devuelve en formato de headers
def get_header_labels(table=None):
    headers = {}
    for field in db[table].fields:
        headers[table+'.'+field] = db[table][field].label
    headers[table+'.id']= 'Número'
    return headers

#transforma los titulos de los formularios genericos
def obtenerTitulo(titulo=None):
    if titulo =='tipoVino':
       titulo = 'tipo de vino'
    elif  titulo =='formaPago':
       titulo = 'Forma de Pago'
    else:
       pass
    return titulo

##############################################################################
################## Metodo utilizado en ABM.py ################################
def abm(tabla_req=None):
    response.view = "%s/%s.%s" % (request.controller, 'abm', request.extension)

    form=SQLFORM(db[tabla_req], submit_button='Enviar')
    if form.accepts(request.vars,session):
        response.flash='Registro ingresado exitosamente '
    elif form.errors:
        response.flash='Complete el formulario '
    else:
        pass
    t = obtenerTitulo(tabla_req)
    titulo = T(' Administración de %s' % t)
    headersT = get_header_labels(tabla_req)

    regs=db(db[tabla_req].id>0).select()

    return locals()#{'titulo': titulo, 'regs':regs, 'form':form, 'headersT':headersT}
