# -*- coding: utf-8 -*-
def bodegaAbm(): return abm('bodega')

def categoriaAbm(): return abm('categoria')


def eventoAbm(): return abm('evento')

def promocionAbm(): return abm('promocion')

def tipoVinoAbm(): return abm('tipoVino')

def varietalAbm(): return abm('varietal')

def formaPagoAbm(): return abm('formaPago')

def zonaAbm(): return abm('zona')


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

#obtiene los Labels de la bd y lo devuelve en formato de headers
def get_header_labels(table=None):
    headers = {}
    for field in db[table].fields:
        headers[table+'.'+field] = db[table][field].label
    headers[table+'.id']= 'Número'
    return headers

def edicion():
    tabla_req = request.args[0]
    form=SQLFORM(db[tabla_req], request.args[1], submit_button=T('Save'))
    #,buttons=[TAG.button('Guardar',_type="submit"),A("Volver",_class='btn btn-default',_onClick="return confirm('desea volver')", _href=URL('abm','%sAbm'%tabla_req ))])

    if form.accepts(request.vars,session):
        session.flash=' Modificado correctamente '
        redirect(URL('abm', '%sAbm'%tabla_req ))
    elif form.errors:
        response.flash=' Complete el formulario '
    else:
        pass
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s');"%URL('abm','%sAbm'%tabla_req ), _class="resetType" )
    
    t = obtenerTitulo(tabla_req)
    titulo = T(' Modificación de %s' % t)
    return locals()#{'titulo': titulo, 'form':form }

def obtenerTitulo(titulo=None):
    if titulo =='tipoVino':
       titulo = 'tipo de vino'
    elif  titulo =='formaPago':
       titulo = 'Forma de Pago'
    else:
       pass
    return titulo
