# -*- coding: utf-8 -*-
def bodegaAbm(): return abm('bodega')

def categoriaAbm(): return abm('categoria')

def eventoAbm(): return abm('evento')

def promocionAbm(): return abm('promocion')

def tipoVinoAbm(): return abm('tipoVino')

def varietalAbm(): return abm('varietal')

def formaPagoAbm(): return abm('formaPago')

def zonaAbm(): return abm('zona')

#################################################
#################### Edicion ####################

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
    form.add_button('Cancelar', "javascript:return confirmarCancelar('%s', this);"%URL('abm','%sAbm'%tabla_req ))
    t = obtenerTitulo(tabla_req)
    titulo = T(' Modificación de %s' % t)
    return locals()#{'titulo': titulo, 'form':form }
