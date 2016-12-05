# -*- coding: utf-8 -*-

#unique=True, bug https://groups.google.com/forum/#!topic/web2py/PLoVjDti-lE
#db.categoria.truncate()

#Categoria: vinos/accesorios/espumantes/
db.define_table('categoria',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    format = '%(nombre)s')
db.categoria.nombre.requires=[IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                              IS_NOT_IN_DB(db, 'categoria.nombre',error_message='Ya existe')]
db.categoria.id.label='Número'

#TipoVinos : blanco, oporto, rosado, dulces, tardio, tinto, etc.
db.define_table('tipoVino',
    Field('tipo', 'string',  required=True, notnull=True, label=T('Tipo de vino') ),
    format = '%(tipo)s')
db.tipoVino.tipo.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                             IS_NOT_IN_DB(db, 'tipoVino.tipo',error_message='Ya existe')]
db.tipoVino.id.label='Número'

#Varietal:malbec, syrah, tempranillo
db.define_table('varietal',
    Field('tipoVarietal', 'string', required=True, notnull=True, label=T('Varietal') ),
    format = '%(tipoVarietal)s')
db.varietal.tipoVarietal.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el varietal '),
                                     IS_NOT_IN_DB(db, 'varietal.tipoVarietal',error_message=' Ya existe ')]
db.varietal.id.label='Número'

#Bodega
db.define_table('bodega',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('descripcion', 'text', label=T('Descripción')),
    Field('web', 'string', label=T('Página Web')),
    format = '%(nombre)s')
db.bodega.nombre.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el nombre'),
                             IS_NOT_IN_DB(db, 'bodega.nombre',error_message='Ya existe')]
db.bodega.id.label='Número'

#Productos: vinos, copas, etc.
db.define_table('producto',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('categoria', 'reference categoria', required=True, notnull=True, label=T('Categoría') ),
    Field('tipo', 'reference tipoVino', label=T('Tipo') ),
    Field('varietal', 'reference varietal',  label=T('Varietal') ),
    Field('descripcion', 'text', label=T('Descripción') ),
    Field('origen', 'string',  label=T('Origen') ),
    Field('anio', 'string',  label=T('Año') ),
    Field('bodega', 'reference bodega',  label=T('Bodega') ),
    Field('cantidad', 'integer', label=T('Cantidad') ),
    Field('precioCompra', 'decimal(9,2)', label=T('Precio compra') ),
    Field('precioVenta', 'decimal(9,2)', label=T('Precio venta') ),
    Field('imagen', 'upload', label=T('Imagen'),autodelete=True),#, uploadfolder=os.path.join(request.folder,'static/temp') ),
    )
db.producto.nombre.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el nombre '),
                               IS_NOT_IN_DB(db, 'producto.nombre', error_message=' Ya existe ')]
db.producto.tipo.requires = IS_IN_DB(db,db.tipoVino.id, '%(tipo)s')
db.producto.categoria.requires = IS_IN_DB(db,db.categoria.id, '%(nombre)s')
db.producto.varietal.requires = IS_IN_DB(db,db.varietal.id, '%(tipoVarietal)s')
db.producto.bodega.requires = IS_IN_DB(db,db.bodega.id, '%(nombre)s')
db.producto.cantidad.requires = IS_INT_IN_RANGE(0, 1e100)
db.producto.precioCompra.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.precioVenta.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.id.label='Número'
db.producto.nombre.writable = True
db.producto.tipo.writable = True

#Promociones por compras en la página
db.define_table('promocion',
    Field('promo', 'string', required=True, notnull=True, label=T('Promoción') ),
    Field('descripcion', 'string', label=T('Descripción')),
    Field('letraChica', 'string', label=T('Lectra chica')),
    Field('fechaDesde', 'date', label=T('Fecha desde')),
    Field('fechaHasta', 'date', label=T('Fecha hasta')),
    )
db.promocion.promo.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar la promo'),
                              IS_NOT_IN_DB(db, 'promocion.promo', error_message=' Ya existe ')]
db.promocion.id.label='Número'
#db.promocion.fechaHasta.requires = IS_DATE_IN_RANGE(format=T('%d-%m-%y'),
#                                                    minimum=form.vars.fechaDesde,
#                                                    maximum=None,
#                                                    error_message='a')
########################################################################
