$(function(){
	$('#dp2').datepicker();
	$('#dp3').datepicker();
});

function showHint(str)
{
	var xmlhttp;
	if (str.length==0)
	{ 
		document.getElementById("text").innerHTML="";
		return;
	}
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			/*document.getElementById("text").innerHTML=xmlhttp.responseText;*/
		}
	}
	xmlhttp.open("GET","gethint.asp?q="+str,true);
	xmlhttp.send();
}

function my_callback(data){
	    alert(data.message);
}
