
/**
 * Para agregar un item al menu ingresar del layout 
 */
function agregarMenuIngresar(texto,url,icono) {
    var divisor = $('.navbar-nav li ul li.divider')[0];
    var elem = $('<li><a href="'+url+'" rel="nofollow"><i class="icon icon-envelope glyphicon glyphicon-envelope"></i> '+texto+'</a></li>')[0];
    divisor.parentNode.insertBefore(elem, divisor);
}

function confirmarCancelar(url, obj) {
    obj.type='reset';
    var x = confirm('Desea volver sin guardar los cambios?');
    if (x) {
        window.location = url;
    }
    return x;
}