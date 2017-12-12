function checkInput(){
	if( document.getElementById("uploadfile").files.length == 0 ){
		document.getElementById("submitarea").style.visibility = "hidden";
	} else {
		document.getElementById("submitarea").style.visibility = "visible";
		console.log("file selected");
	}
}