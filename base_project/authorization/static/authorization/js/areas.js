
var measure;

$(document).ready(function() { });


// Obtiene coordenadas de la posición dle usuario
function getCoords(position){
	// var lat = position.coords.latitude;
	// var lng = position.coords.longitude;

	// initialize(lat,lng

	// Obtiene lista de parcelas para iniciar el mapa en la primera.
	$.get(window.location.origin+"/data_fields",{},function(data_fields){

		var field_objects = $.parseJSON(data_fields);

		initialize(field_objects[0].centerlatitude, field_objects[0].centerlongitude);
	});

}

// Referencia cuando ocurre error al obtener posición actual
function getError(err) {
	// Coordenadas de Los Mochis
	initialize(25.7837843,-109.0605664);
}

// Inicializa Mapa
function initialize(lat, lng){

	measure = {
		mvcMarkers: new google.maps.MVCArray(),
		line: null,
		polygon: null
	};

	var mapOptions = {
		scaleControl: true,
		zoom: 8,
		zoomControl: true,
		zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL},
		panControl: false,
		center: new google.maps.LatLng(lat, lng),
		mapTypeId: google.maps.MapTypeId.HYBRID,
		draggableCursor: 'crosshair'
	};

	// Mapa
	map = new google.maps.Map($("#mapa").get(0), mapOptions);
	getFields(map);
}

//
function geocodeResult(results, status){
	if(status=='OK'){
		initialize(results[0].geometry.location.lat(), results[0].geometry.location.lng());
	}
}


// Agrega Marcador al Mapa
function marcador(field, map){

	return new google.maps.Marker({
		position : new google.maps.LatLng(field.centerlatitude,field.centerlongitude),
		map : map,
		draggable :false,
		clickable: true,
		title : field.name
	});
}

// Obtiene Datos de Parcelas
function getFields(map){
	$.get(window.location.origin+"/data_fields",{},function(data_fields){

		var field_objects = $.parseJSON(data_fields);

		$.each(field_objects, function(x, item) {
			var marc = marcador(item, map);
			infoWindow(marc, item);
		});
	});
}

// Crea Cuadro de Información
function infoWindow(marc, field){

	datos = {
		'latitude':marc.getPosition().lat(),
		'longitude':marc.getPosition().lng(),
		'field_id': field.id,
	}

	// Post para datos de clima
	$.post(window.location.origin+'/data_field_climate', datos, function(datos){
        console.log(datos);
		var infowindow = new google.maps.InfoWindow({
			content: datos,
			maxWidth: 450
		});

		marc.addListener('click', function() {
			infowindow.open(map, marc);
		});
	});
}
