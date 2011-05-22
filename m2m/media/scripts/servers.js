function moreHandler(){
	$('.togglebot').click(function(){
		var togglerID = $(this).attr('id');
		var id = togglerID.substr(0,togglerID.length - 1);
		$('#'+id).slideToggle("slow");
		$('#'+id+'s').slideToggle("slow");
		$(this).text($(this).text() == 'More...' ? 'Less...' : 'More...');
	});
}

$(document).ready(function(){
	moreHandler();
});