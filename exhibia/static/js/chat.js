chat_socket = io.connect('/chat');
$(document).ready(function(){
    $('#chat .tab-title').click(function() {
            $('#chat .container').toggle();
    });
    // User hits enter
    $('#chat-msg').keyup(function(e){
        var code = e.which;

        if(code==13) {
            socket.emit('send_chat_message', $(this).val());
            $(this).val('');
        }
    });
    var adaptSidebar = function() {
        // Chat is displayed as a sidebar
        var chat_height         = $('#chat').outerHeight();
        var video_stream_height = (!$('.video-stream').is(':visible')) ? 0 : $('.video-stream').height();
        var chat_content_height = $('.chat-content').outerHeight();
        var divisors            = $('#chat .divisor').length;
        var diff = (chat_height - (video_stream_height + chat_content_height + (8 * divisors)));
        $('.social-stream').css('height', diff - 70);
    }

    var body_width = $('body').outerWidth();
    if(body_width > 1000) {
        adaptSidebar();
    }

    $(window).on('resize', adaptSidebar);

    $('#chat .divisor').click(function() {
        $('.video-stream').toggle();
        $('.chat-content').toggleClass('no-video');
        adaptSidebar();
    });


    chat_socket.on('user_message', function(username, message, picture){
        var chat_msg = $('<li />').addClass('row').hide();
            chat_msg.html('<div class="span1"><img src="' + picture +'" class="img-circle" title="'+ username +'" /></div><div class="span2"><span class="user-name">' + username +'</span>' + message +'</div>');
       $('#chat .chat-container').prepend(chat_msg);
            chat_msg.slideDown();
    });
    chat_socket.on('notification', function (msg) {
        insert_notification(msg);
    });

});
