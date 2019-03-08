

document.querySelect('.user').style.animationPlayState = "paused";

var link = document.querySelectall("a");

for(i=0;i<link.length;i++){
	link[i].addEventListener('onClick', user())
}

function user(){
	document.querySelect('.user').style.animationPlayState = "running";
}