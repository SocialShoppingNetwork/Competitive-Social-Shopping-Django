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



    chat_socket.on('user_message', function(username, message, picture, twitter_verified,
                                            google_verified, facebook_verified, is_winner) {

         message = $('<div class="comment"></div>').text(message).html();

         var chat_msg =
             '<li>' +
                '<div class="foto"><img src="' + picture + '"/></div>' +
                '<div class="description">' +
                    '<table>' +
                        '<tr>' +
                            '<td>' +
                                '<a href="#">' + username + '</a>' +
                            '</td>';

         if (twitter_verified) {
            chat_msg += '<td><i class="icon-twitter"></i></td>'
         }
         if (google_verified) {
             chat_msg += '<td><i class="icon-google"></i></td>'
         }
         if (facebook_verified) {
             chat_msg += '<td><i class="icon-facebook"></i></td>'
         }
         if (is_winner) {
             chat_msg += '<td><i class="icon">W</i></td>'
         }

         chat_msg +=
                 '</tr>' +
                    '</table>' +
                        message +
                '</div></li>';

        var chat_messages = $('.chat-messages');
        chat_messages.append(chat_msg);
        chat_messages.scrollTop(chat_messages.prop('scrollHeight'));

    });
    chat_socket.on('notification', function (msg) {
        insert_notification(msg);
    });

});
