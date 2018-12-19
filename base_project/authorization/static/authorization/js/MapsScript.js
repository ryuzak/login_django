
$(function(){
	
	// si el navegador cuenta con geolocalizacion hace una llamada a getCurrentPosition
	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(getCoords, getError);
	}else{
		alert('no cuenta con sistema de geolocalizacion');
	}

 });
