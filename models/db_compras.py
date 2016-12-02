# -*- coding: utf-8 -*-
db.define_table("formaPago",
                Field("descripcion", "string", label=T('Descripción'),required=True, notnull=True),
                )
db.formaPago.descripcion.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar la forma de pago '),
                                     IS_NOT_IN_DB(db, 'formaPago.descripcion', error_message=' Ya existe ')]
db.formaPago.id.label='Número'

#zonas de entrega
db.define_table("zona",
                Field("descripcion", "string", required=True, notnull=True, label=T('Descripción')),
                Field("precio", "string", required=True, notnull=True, label=T('Costo')),
                )
db.zona.descripcion.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar descripción '),
                                IS_NOT_IN_DB(db, 'zona.descripcion', error_message=' Ya existe ')]


#Domicilios
db.define_table("domicilio",
                Field("idCliente", "reference auth_user", required=True, notnull=True, label=T('Cliente Nro ')),
                Field("calle", "string", required=True, notnull=True, label=T('Calle')),
                Field("numero", "integer", required=True, notnull=True, label=T('Nro ')),
                Field("piso", "string", label=T('Piso')),
                Field("departamento", "string", label=T('Depto')),
                Field("otros", "string", label=T('Otros ')),
                Field("idZona", "reference zona", required=True, notnull=True, label=T('Zona')),
                )
db.domicilio.idCliente.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar descripción '),
                                   IS_IN_DB(db, "auth_user.id"," %(last_name)s - %(first_name)s ")]
db.domicilio.idZona.requires = IS_IN_DB(db, 'zona.id', " %(descripcion)s" )


############################################################################################################################
#ventas basico
db.define_table("venta",
    Field("idCliente", 'reference auth_user', required=True, notnull=True, label=T('Cliente Nro') ),
    Field("tipoFactura","string", required=True, notnull=True, label=T('Tipo de Factura') ),
    Field("fechaPedido","date", required=True, notnull=True, label=T('Fecha Pedido') ),
    Field("importeTotal","string", required=True, notnull=True, label=T('Importe Total') ),
    Field("formaPago", 'reference formaPago', required=True, notnull=True, label=T('Forma de pago') ),
    Field("formaEntrega", 'string', required=True, notnull=True, label=T('Forma de entrega') ),
    Field("costoEntrega", 'double', required=True, notnull=True, label=T('Costo de entrega') ),
    Field("idDomicilio", "reference domicilio", required=True, notnull=True, label=T('Domicilio')),
)

db.venta.idCliente.requires = IS_IN_DB(db, "auth_user.id"," %(last_name)s - %(first_name)s ")
db.venta.tipoFactura.requires=IS_IN_SET(["A","B"])
db.venta.formaPago.requires = IS_IN_DB(db, "formaPago.id"," %(descripcion)s ")
db.venta.id.label ='Número'
db.venta.formaEntrega.requires=IS_IN_SET(["Retiro en local","Entrega a domicilio"])

#Detalle ventas
db.define_table("detalleVenta",
    Field("idVenta","integer", required=True, notnull=True, label=T('Nro de Venta ') ),
    Field("idProducto","integer", required=True, notnull=True, label=T('Producto ') ),
    Field("cantidad","integer", required=True, notnull=True, label=T('Cantidad ') ),
    Field("precioUnitario","double", required=True, notnull=True, label=T('Precio unidad ') ),
    Field("descuento","double", required=True, notnull=True, label=T('Descuento') ),
    )


#db.detalleVenta.idProducto.requires = IS_IN_DB(db,"producto.idProducto", " %(nombre)s" )
#db.detalleVenta.precioUnitario.requires = IS_IN_DB(db,"producto.precio_venta","%(precio_venta)s")
#db.detalleVenta.id_venta.requires = IS_IN_DB(db,"ventas.id","%(numero_factura)s-%(tipo_de_factura)s")
#db.detalleVenta.id.label ='Número'
