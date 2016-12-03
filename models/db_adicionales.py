#unique=True, bug https://groups.google.com/forum/#!topic/web2py/PLoVjDti-lE
#db.categoria.truncate()

#Categoria: vinos/accesorios/espumantes/
db.define_table('categoria',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') )
    )
db.categoria.nombre.requires=[IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                              IS_NOT_IN_DB(db, 'categoria.nombre',error_message='Ya existe')]
db.categoria.id.label='Número'

#TipoVinos : blanco, oporto, rosado, dulces, tardio, tinto, etc.
db.define_table('tipoVino',
    Field('tipo', 'string',  required=True, notnull=True, label=T('Tipo de vino') ),
    )
db.tipoVino.tipo.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el tipo'),
                             IS_NOT_IN_DB(db, 'tipoVino.tipo',error_message='Ya existe')]
db.tipoVino.id.label='Número'

#Varietal:malbec, syrah, tempranillo
db.define_table('varietal',
    Field('tipoVarietal', 'string', required=True, notnull=True, label=T('Varietal') ),
    )
db.varietal.tipoVarietal.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el varietal '),
                                     IS_NOT_IN_DB(db, 'varietal.tipoVarietal',error_message=' Ya existe ')]
db.varietal.id.label='Número'

#Bodega
db.define_table('bodega',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('descripcion', 'text', label=T('Descripción')),
    )
db.bodega.nombre.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el nombre'),
                             IS_NOT_IN_DB(db, 'bodega.nombre',error_message='Ya existe')]
db.bodega.id.label='Número'
db.bodega.nombre.writable = True
db.bodega.descripcion.writable = True

#noticias
db.define_table('noticia',
    Field('titulo', 'string', required=True, notnull=True, label=T('Titulo') ),
    Field('copete', 'string', label=T('Copete')),
    Field('cuerpo', 'text', label=T('Cuerpo')),
    Field('autor', 'string', label=T('Autor')),
    Field('fecha', 'date', label=T('Fecha')),
    #Verificar como se guardan las imagenes
    Field('imagen', 'upload', label=T('Imagen'), autodelete=True),
    )
db.noticia.titulo.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar el titulo'),
                              IS_NOT_IN_DB(db, 'noticia.titulo', error_message=' Ya existe ')]
db.noticia.id.label='Número'

#Eventos
db.define_table('evento',
    Field('nombre', 'string', required=True, notnull=True, label=T('Nombre') ),
    Field('caracteristicas', 'text', label=T('Características')),
    Field('requisitos', 'text', label=T('Requisitos')),
    Field('fecha', 'date', label=T('Fecha')),
    Field('hora', 'time', label=T('Horario')),
    Field('duracion', 'decimal(2,2)', label=T('Duración')),
    )
db.evento.nombre.requires = [IS_NOT_EMPTY(error_message='Falta ingresar el nombre'),
                             IS_NOT_IN_DB(db, 'evento.nombre', error_message=' Ya existe ')]
db.evento.duracion.requires = IS_DECIMAL_IN_RANGE(0,200)
db.evento.id.label='Número'

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
db.producto.tipo.requires = IS_IN_DB(db,db.tipoVino.id, "%(tipo)s")
db.producto.categoria.requires = IS_IN_DB(db,db.categoria.id, "%(nombre)s")
db.producto.varietal.requires = IS_IN_DB(db,db.varietal.id, "%(varietal)s")
db.producto.bodega.requires = IS_IN_DB(db,db.bodega.id, "%(nombre)s")
db.producto.cantidad.requires = IS_INT_IN_RANGE(0, 1e100)
db.producto.precioCompra.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.precioVenta.requires = IS_DECIMAL_IN_RANGE(1, 1e100)
db.producto.id.label='Número'

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

########################################################################
