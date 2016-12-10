# -*- coding: utf-8 -*-

#noticias
db.define_table('noticia',
    Field('titulo', 'string', required=True, notnull=True, label=T('Titulo') ),
    Field('copete', 'string', label=T('Copete')),
    Field('cuerpo', 'text', label=T('Cuerpo')),
    Field('autor', 'string', label=T('Autor')),
    Field('fecha', 'date', label=T('Fecha')),
    Field('imagen', 'upload', label=T('Imagen'), autodelete=True),
    format = '%(titulo)s')
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
db.evento.hora.requires = IS_TIME(error_message='Debe ser HH:MM:SS!')
db.evento.duracion.requires = IS_DECIMAL_IN_RANGE(0,200)
db.evento.id.label='Número'
