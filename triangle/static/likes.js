$(document).ready(function() {
	$('.like-btn').on("click", function(event) {
		let post = $(this).attr("post-data");
		$.get(window.location.url, {"post-data": post}, function(data, status) {
			$(this).hide();
			console.log(window.location.url);
		});
	});
});
