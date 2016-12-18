/**
 * Para agregar un item al menu ingresar del layout
 */
function agregarMenuIngresar(contenido,iconos,url) {
    var divisor = $('.navbar-nav li ul li.divider')[0];
    var elem = undefined
    if (url==undefined)
        elem = $('<li>'+contenido+'</li>')[0];
    else
        elem = $('<li><a href="'+url+'" rel="nofollow"><i class="'+iconos+'"></i> '+contenido+'</a></li>')[0];
    divisor.parentNode.insertBefore(elem, divisor);
}

function confirmarCancelar(url, obj) {
    obj.type='reset';
    var x = confirm('Desea volver sin guardar los cambios?');
    if (x&&url!=null) {
        window.location = url;
    }
    return x;
}
