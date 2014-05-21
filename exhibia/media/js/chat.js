chat_socket = io.connect('/chat');
$(document).ready(function(){
    // User hits enter
    $('#chat-msg').keyup(function(e){
        var code = e.which;
        var text = $.trim($(this).val());
        if(code==13 && text) {
            chat_socket.emit('send_chat_message', text);
            $(this).val('');
        }
    });

    chat_socket.on('user_message', function(username, message, picture) {
       var chat_msg = $('<li />').hide();
            chat_msg.html('<div class="foto"><img src="' + picture + '"/></div>' +
                '<div class="description">' +
                    '<table>' +
                        '<tr>' +
                            '<td>' +
                                '<a href="#">' + username + '</a>' +
                            '</td>' +
                            '<td>' +
                                '<i class="icon-ok-circled"></i>' +
                            '</td>' +
                            '<td>' +
                            '</td>' +
                       '</tr>' +
                    '</table>' +
                    '<div class="comment">' +
                    message +
                    '</div>' +
                '</div>'
            );

       $('#chat-msg').closest('li').prepend(chat_msg);
            chat_msg.slideDown();

    });
    chat_socket.on('notification', function (msg) {
        insert_notification(msg);
    });

});
