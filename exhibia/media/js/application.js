jQuery(document).ready(function($) {

	//button-top
	console.log("huioioio");
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#go-up').show();
            ;
        } else {
            $('#go-up').hide();
        }
    });
    $('#go-up').click(function () {
        $('.header').ScrollTo(0);
    });
	


});