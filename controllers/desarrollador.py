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
def limpiarUsers():
	db.auth_user.truncate()
	response.flash='Tabla usuarios truncada'
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

def poblarCategoria():
    #Categorias
    db.categoria.insert(nombre='Accesorios')
    db.categoria.insert(nombre='Cristalería')
    db.categoria.insert(nombre='Vinos')
    return True
def poblarVarietal():
    #varieltal
    db.varietal.insert(tipoVarietal='Albariño')
    db.varietal.insert(tipoVarietal='Bonarda')
    db.varietal.insert(tipoVarietal='Cabernet Franc')
    db.varietal.insert(tipoVarietal='Cabernet Sauvignon')
    db.varietal.insert(tipoVarietal='Corte')
    db.varietal.insert(tipoVarietal='Chardonnay')
    db.varietal.insert(tipoVarietal='Gewürztraminer')
    db.varietal.insert(tipoVarietal='Malbec')
    db.varietal.insert(tipoVarietal='Merlot')
    db.varietal.insert(tipoVarietal='Nebbiolo')
    db.varietal.insert(tipoVarietal='Petit Verdot')
    db.varietal.insert(tipoVarietal='Pinot Grigio')
    db.varietal.insert(tipoVarietal='Riesling')
    db.varietal.insert(tipoVarietal='Sauvignon Blanc')
    db.varietal.insert(tipoVarietal='Syrah')
    db.varietal.insert(tipoVarietal='Tannat')
    db.varietal.insert(tipoVarietal='Tempranillo')
    db.varietal.insert(tipoVarietal='Torrontés')
    db.varietal.insert(tipoVarietal='Viognier')
    db.varietal.insert(tipoVarietal='Zinfandel')
    response.flash='varietal fue poblada'
    return True
def poblarTipoVino():
    #tiposVino
    db.tipoVino.insert(tipo ='Blanco')
    db.tipoVino.insert(tipo ='Espumante')
    db.tipoVino.insert(tipo ='Rosado')
    db.tipoVino.insert(tipo ='Tardío')
    db.tipoVino.insert(tipo ='Tinto')
    response.flash='Fue poblada tipoVino'
    return True

def poblarBodegas():
    db.bodega.insert(nombre = 'Bodega Ruca Malen',
                     descripcion = 'Es una Bodega Boutique de capitales franceses. Su dueño Jean Pierre Thibaud fue presidente de Chandon Argentina por 10 años. Ubicada en la zona de Agrelo, Luján de Cuyo.',
                     web='www.bodegarucamalen.com.ar')
    db.bodega.insert(nombre = 'Bodega Tapiz',
                     descripcion = 'Bodega perteneciente a una familia argentina. En la visita se hace hincapié en los viñedos, sobre todo comparando las distintas variedades, también se degustan vinos con roble francés y roble americano para apreciar las diferencias. Ubicada en la zona de Luján de Cuyo.',
                     web='www.fincaspatagonicas.com')
    db.bodega.insert(nombre = 'Bodega CarinaE',
                     descripcion = 'Bodega Boutique, perteneciente a un matrimonio francés, Philippe y Brigitte Subra. Elaboración pequeña de alta calidad. Ubicada en la zona de Maipú.',
                     web='www.carinaevinos.com')
    db.bodega.insert(nombre = 'Finca Decero',
                     descripcion = 'Moderna y tecnológica Bodega con producción de vinos de alta gama, se destaca el Petit Verdot con una increíble arquitectura y una vista privilegiada a la Cordillera de Los Andes. Ubicada en la zona de Luján de Cuyo.',
                     web='www.decero.com')
    db.bodega.insert(nombre = 'Domaine St Diego',
                     descripcion = 'Bodega Boutique, pertenece a uno de los enólogos mas reconocidos de Argentina, Ángel Mendoza y nos recibirán sus propios dueños. Ubicada en la zona de Maipú.',
                     web='')
    db.bodega.insert(nombre = 'Bodega Norton',
                     descripcion = 'Es una de las bodegas más tradicionales de la Argentina, hoy en manos de la familia Swarovski de Austria. Ubicada en la zona de Luján de Cuyo.',
                     web='www.norton.com.ar')
    db.bodega.insert(nombre = 'Bodega Achaval Ferrer',
                     descripcion = 'Pequeña Bodega que elabora vinos de excelente calidad. Ha obtenido un alto puntaje en la prestigiosa revista Wine Spectator, con sus vinos Altamira y Quimera. Ubicada en la zona de Luján de Cuyo.',
                     web='www.achaval-ferrer.com')
    db.bodega.insert(nombre = 'Bodega Lagarde',
                     descripcion = 'Tradicional bodega, la cual sigue en manos de una familia mendocina. Una característica importante es el método de elaboración del Espumante, utilizan el tradicional método Champenoise. Ubicada en la zona de Luján de Cuyo.',
                     web='www.lagarde.com.ar')
    db.bodega.insert(nombre = 'Bodega Altavista',
                     descripcion = 'Bodega de capitales franceses. Refaccionaron una Bodega antigua donde siguen utilizando las piletas de concreto, para los vinos de alta gama. Ubicada en la zona de Luján de Cuyo.',
                     web='www.altavistawines.com')
    db.bodega.insert(nombre = 'El Lagar de Carmelo Patti',
                     descripcion = 'Bodega pequeña, donde Carmelo elabora unos de los mejores vinos de Mendoza. Hay que destacar el Cabernet Sauvignon y su Gran Assemblage, combinación de 4 variedades (Cabernet Sauvignon, Malbec, Merlot y Cabernet Franc). Él mismo recibe a quien lo visita, transmitiéndoles su pasión por los vinos. Ubicada en la zona de Luján de Cuyo.',
                     web='')
    db.bodega.insert(nombre = 'Bodega Catena Zapata',
                     descripcion = 'Es una de las bodegas mas reconocidas internacionalmente. La arquitectura es algo a destacar con su forma de pirámide Maya. Ubicada en la zona de Luján de Cuyo.',
                     web='')
    db.bodega.insert(nombre = 'Bodega Benegas',
                     descripcion = 'Antigua bodega mendocina, completamente restaurada, perteneciente a la familia Benegas. Ubicada en la zona de Luján de Cuyo.',
                     web='www.bodegabenegas.com')
    db.bodega.insert(nombre = 'Bodega Dominio del Plata',
                     descripcion = 'Bodega Boutique perteneciente a Susana Balbo, enóloga y Pedro Marchevsky, Ingeniero agrónomo. Elaboran vinos de alta gama muy reconocidos en el mercado internacional. Ubicada en la zona de Luján de Cuyo.',
                     web='www.dominiodelplata.com.ar')
    db.bodega.insert(nombre = 'Bodega Melipal',
    				 descripcion = 'Moderna y tecnificada Bodega Boutique, elabora exclusivamente la variedad Malbec. Ubicada en la zona de Luján de Cuyo.',
                     web='www.bodegamelipal.com')
    db.bodega.insert(nombre = 'Belasco de Baquedano',
    				 descripcion = 'Ubicada en la zona de Agrelo. Perteneciente a una familia de España, la cual posee bodega',
                     web='www.grupolanavarra.com')
    db.bodega.insert(nombre = 'Walter Bressia',
    				 descripcion = 'Perteneciente al reconociddo enólogo Walter Bressia, es una pequeña bodega, ubicada en el corazón de Agrelo. Algunos de sus vinos: Bressia Profundo, Lágrima Canela.',
                     web='www.bressiabodega.com')
    db.bodega.insert(nombre = 'CAP Vistalba',
    				 descripcion = 'Moderna bodega, perteneciente a Carlos Pulenta, familia ligada la historia de la vitivinicultura argentina. Algunos de sus vinos: Corte A, Corte B, Corte C.',
                     web='www.carlospulentawines.com')
    db.bodega.insert(nombre = 'Clos de Chacras',
    				 descripcion = 'Pertenece a una familia de Mendoza. Es una antigua bodega renovada tecnológicamente, para obtener vinos de a lta calidad. Ganadora del premio Argentina Wine Awards.',
                     web='www.closdechacras.com.ar')
    db.bodega.insert(nombre = 'Cassone',
    				 descripcion = 'Bodega boutique, perteneciente a la familia Cassone. Algunos de sus vinos: Obra Prima and La Florencia.',
                     web='www.familiacassone.com.ar')
    db.bodega.insert(nombre = 'Chandon',
    				 descripcion = 'Una de las primeras bodegas del exterior que llegó a Argentina. Conocida por sus excelentes espumantes, también elabora vinos tintos y blancos.',
                     web='www.chandon.com.ar')
    db.bodega.insert(nombre = 'Luigi Bosca',
    				 descripcion = 'Tradicional bodega, perteneciente a una de las familias con más historia enológica, Arizu. Produce vinos de altisima calidad. Sus vinos están en las vinotecas de varios países.',
                     web='www.luigibosca.com.ar')
    db.bodega.insert(nombre = 'Renacer',
    				 descripcion = 'Bodega boutique que pertenece a un bodeguero de Chile. Elabora sólo Malbec de alta calidad. Algunos de sus vinos: PUnto Final, Punto Final Reserva, Enamore y su vino top Renacer.',
                     web='www.bodegarenacer.com.ar')
    db.bodega.insert(nombre = 'Terrazas de Los Andes',
    				 descripcion = 'Pertenece al grupo Chandon. Una de sus características, son las diferentes terrazas donde cultivan los viñedos para sus vinos de alta calidad.',
                     web='www.terrazasdelosandes.com')
    db.bodega.insert(nombre = 'Tempus Alba',
    				 descripcion = 'Moderna bodega, ubicada en Maipú. Posee la última tecnología para producir vinos de alta calidad.',
                     web='www.tempusalba.com')
    db.bodega.insert(nombre = 'Familia Zuccardi',
    				 descripcion = 'Una de las bodegas con más presencia en el exterior. Pertenece a José Zuccardi, quen ha construído una familiar bodega industrial. Algunos de sus vinos: Santa Julia, Z, Q, Malamado, Magna.',
                     web='www.familiazuccardi.com')
    db.bodega.insert(nombre = 'Don Bosco',
    				 descripcion = 'Una de las bodegas con más historia, ya que ahí funciona una de las mas prestigiosas Facultades de Enología. Fue la primera de América. Su visita es muy interesante, un viaje al pasado y a la tradición.',
                     web='')
    db.bodega.insert(nombre = 'Nieto Senetiner',
    				 descripcion = 'Pertenecía a la familia Nieto, luego fue adquirida por un importante grupo económico. Algunos de sus vinos: Nieto Senetiner, Don Nicanor, Benjamin Nieto, y el prstigioso Cadus.',
                     web='www.nietosenetiner.com.ar')
    db.bodega.insert(nombre = 'Pulenta Estate',
                     descripcion = 'Moderna Bodega la cual elabora vinos Premium. Ubicada en Alto Agrelo, una zona con mucho potencial en la Argentina.',
                     web='www.pulentaestate.com')
    db.bodega.insert(nombre = 'Bodega Altus',
                     descripcion = 'En esta Bodega restauraron una casona antigua, donde reciben a los invitados para almorzar, su nombre es “La Tupiña”, cuenta con un ambiente muy cálido y acogedor. Ubicada en la zona de Valle de Uco.',
                     web='')
    db.bodega.insert(nombre = 'Andeluna Cellars',
                     descripcion = 'Bodega perteneciente a Ward Lay, empresario norteamericano. Posee un encanto natural, ya que tiene una increíble vista a la Cordillera de Los Andes. Ubicada en la zona de Valle de Uco.',
                     web='www.andeluna.com')
    db.bodega.insert(nombre = 'Bodega Salentein',
                     descripcion = 'Fue una de las primeras bodegas en instalarse en la zona de Valle de Uco. Posee una increíble arquitectura. La cava es algo para destacar. Es de capitales holandeses. Cuenta también con una sala de arte llamada Kilka, donde se exponen obras de artistas nacionales y extranjeros.',
                     web='www.bodegasalentein.com')
    db.bodega.insert(nombre = 'The Vines of Mendoza',
                     descripcion = 'Distribuidos en una superficie de 202 hectáreas en el prestigioso Valle de Uco, ofrecen un número limitado de viñedos privados en parcelas de 1,2 a 2 hectáreas administrados por profesionales.',
                     web='www.vinesofmendoza.com')
    db.bodega.insert(nombre = 'Gimenez Riili',
                     descripcion = 'La bodega, ubicada en Los Sauces, Tunuyán (Valle de Uco), posee una capacidad de elaboración de 125.000 litros. Está equipada con maquinaria de última generación, tanques de acero inoxidable y barricas de roble.',
                     web='www.gimenezriilli.com')
    db.bodega.insert(nombre = 'Bodega Lurton',
                     descripcion = 'Los Lurton, estos famosos hermanos franceses eligieron Mendoza, en especial Valle de Uco para instalarse, ya que vieron el potencial de la zona. Esta Bodega está equipada con una alta tecnología. Se puede hacer una degustación de sus tanques.',
                     web='www.jflurton.com')
    db.bodega.insert(nombre = 'Bodega La Azul',
                     descripcion = 'Pequeña Bodega boutique, de capitales argentinos. Elabora vinos de alta gama. Está ubicada en el departamento de Tunuyán con una increíble vista a la montaña.',
                     web='www.bodegalaazul.com.ar')
    db.bodega.insert(nombre = 'Bodega O. Fournier',
                     descripcion = 'Bodega altamente tecnológica. Diseñada totalmente bajo métodos de gravedad. Ubicada en el Departamento de San Carlos, Valle de Uco. Posee un increíble restaurante con vista a la montaña.',
                     web='www.ofournier.com')
    db.bodega.insert(nombre = 'Finca La Celia',
                     descripcion = 'Pertenece a un prestigioso grupo chileno.',
                     web='www.fincalacelia.com.ar')
    db.bodega.insert(nombre = 'Monteviejo',
                     descripcion = 'Pertenece al grupo francés, Clos de los 7. Unos de sus propietarios, es el famoso enólogo Michel Rolland.',
                     web='www.monteviejo.com')
    db.bodega.insert(nombre = 'Cuvelier',
                     descripcion = 'Pertenece al grupo Clos de los 7.',
                     web='')
    response.flash='Fue poblada bodega'
    return True

def poblarFormaPago():
    db.formaPago.insert(descripcion = 'Cheque')
    db.formaPago.insert(descripcion = 'Depósito')
    db.formaPago.insert(descripcion = 'Efectivo')
    db.formaPago.insert(descripcion = 'Tarjeta de Crédito')
    response.flash='Fue poblada formaPago'
    return True

def poblarZonas():
    db.zona.insert(descripcion='A', precio='50', dia='Lunes')
    db.zona.insert(descripcion='B', precio='70', dia='Martes')
    db.zona.insert(descripcion='C', precio='80', dia='Miércoles')
    db.zona.insert(descripcion='D', precio='40', dia='Jueves')
    db.zona.insert(descripcion='E', precio='50', dia='Viernes')
    db.zona.insert(descripcion='F', precio='30', dia='Lunes Viernes')
    response.flash='Fue poblada zona'
    return True
