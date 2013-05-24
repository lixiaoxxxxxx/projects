var onLoad = function(){
	$("input[type='radio']").click(function(){
		$(this).parent().parent().parent().parent().addClass("chosen")
		$.post("classify/",
			{
				"userid":$(this).attr('name'),
				"value":$(this).val()
			},
			function(data){})
	})
}
window.onload = onLoad;
