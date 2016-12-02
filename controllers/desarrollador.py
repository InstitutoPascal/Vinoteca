# -*- coding: utf-8 -*-
def admin():
    return {'titulo': 'Administrar DB'}

def limpiarbodega():
	db.bodega.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarcategoria():
	db.categoria.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarevento():
	db.evento.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarpromocion():
	db.promocion.truncate()
	response.flash='Tabla truncada'
	return True
def limpiartipoVino():
	db.tipoVino.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarvarietal():
	db.varietal.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarformaPago():
	db.formaPago.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarzona():
	db.zona.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarnoticia():
	db.noticia.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarproducto():
	db.producto.truncate()
	response.flash='Tabla truncada'
	return True
def limpiardomicilio():
	db.domicilio.truncate()
	response.flash='Tabla truncada'
	return True
def limpiarventa():
	db.venta.truncate()
	response.flash='Tabla truncada'
	return True
def limpiardetalleVenta():
	db.detalleVenta.truncate()
	response.flash='Tabla truncada'
	return True

def limpiarTODO():
    db.bodega.truncate()
    db.categoria.truncate()
    db.evento.truncate()
    db.promocion.truncate()
    db.tipoVino.truncate()
    db.varietal.truncate()
    db.formaPago.truncate()
    db.zona.truncate()
    db.noticia.truncate()
    db.producto.truncate()
    db.domicilio.truncate()
    db.venta.truncate()
    db.detalleVenta.truncate()
    response.flash='Todas las tablas fueron truncadas'
    return True
