var circle_color = null
var onLoad = function(){
	$("input[type='radio']").click(function(){
		$(this).parent().parent().parent().parent().addClass("chosen")
		$.post("classify/",
			{
				"userid":$(this).attr('name'),
				"value":$(this).val()
			},
			function(data){})
	});
	$("circle").live({
		"mouseover": function(){
			target = $(this).text()
			/* alert($("#" + target).text()) */
			/* $("#" + target).addClass("selected_name") */
			name_color = $("#" + target).css("color")
			name_background = $("#" + target).css("background")
			$("#" + target).css("color", "#fff")
			$("#" + target).css("background", "#000")
			$("#short_name").text($("#" + target).text())
			/* alert($(this).text()) */
		},
		"mouseout": function(){
			target = $(this).text()
			$("#" + target).css("color", name_color)
			$("#" + target).css("background", name_background)
			/* $("#" + target).removeClass("selected_name") */
		}
	})
	$("a").live({
		"mouseover": function(){
			number = $(this).attr('id')
			circle_color=$("circle:contains(" + number + ")").css("fill")
			$("circle:contains(" + number + ")").css("fill", "#000")
		},
		"mouseout": function(){
			number = $(this).attr('id')
			$("circle:contains(" + number + ")").css("fill", circle_color)
		},
	})
}
window.onload = onLoad;

