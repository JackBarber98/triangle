function toggle_visibility(a) {
    var x = document.getElementById('Login');
	var y = document.getElementById('Register');
	var i = document.getElementById('loginbutton');
	var j = document.getElementById('registerbutton');
	
	if(a == "1"){
		y.style.display = 'none';
		x.style.display = 'block';
		i.style.backgroundColor = '#001326';
		j.style.backgroundColor = '#8BB9C1';
	}
	
	if(a == "2"){
		x.style.display = 'none';
		y.style.display = 'block';
		j.style.backgroundColor = '#001326';
		i.style.backgroundColor = '#8BB9C1';
	}
}