def subscribe():
    ''' 
    Por defecto es True
    '''
    suscribir = len(request.args) == 0 or request.args[0]==str(True)
    response.flash = setSuscripcion(suscribir)
    return True