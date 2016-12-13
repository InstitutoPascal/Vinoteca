def subscribe():
    suscribir = False
    if len(request.args) > 0:
        suscribir = bool(request.args[0])
    print suscribir
    response.flash = setSuscripcion(suscribir)
    return True