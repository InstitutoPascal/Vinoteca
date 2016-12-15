# -*- coding: utf-8 -*-
def index():
    try:

        db.venta.insert(idCliente = 4,
                        formaPago = None,
                        importeTotal = None,
                        formaEntrega = None,
                        fechaEntrega = None,
                        costoEntrega = None,
                        idDomicilio = None,
                        estado = None)

        print 'paso'
    except Exception as blumba:
        print blumba
    return tieneCompraVigente
