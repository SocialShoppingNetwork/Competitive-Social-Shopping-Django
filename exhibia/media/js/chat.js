chat_socket = io.connect('/chat');
$(document).ready(function() {
    // User hits enter
    $('#chat-msg').keyup(function(e){
        var code = e.which;
        var text = $.trim($(this).val());
        if(code==13 && text) {
            chat_socket.emit('send_chat_message', text);
            $(this).val('');
        }
    });



    chat_socket.on('user_message', function(username, message, picture, user_id) {

         message = $('<div class="comment"></div>').text(message).html();

         var chat_msg =
             '<li>' +
                '<div class="foto"><img src="' + picture + '"/></div>' +
                '<div class="description">' +
                    '<table>' +
                        '<tr>' +
                            '<td class="user-description-box" data-user-id="' + user_id + '">' +
                                '<a href="#">' + username + '</a>' +
                            '</td>' +
                        '</tr>' +
                    '</table>' +
                    message +
                '</div>' +
             '</li>';

        var chat_messages = $('.chat-messages');
        chat_messages.append(chat_msg);
        chat_messages.scrollTop(chat_messages.prop('scrollHeight'));

    });

    chat_socket.on('notification', function (msg) {
        insert_notification(msg);
    });

    $('body').on('mouseenter', '.user-description-box', function(event) {
        var user_id = $(this).attr('data-user-id');

        if (!user_id) {
            return;
        }

        var _this = this;

        $.ajax({
            type: "GET",
            url: "/account/append_description_box/",
            data: {'user_id': user_id },
            dataType: 'html',
            success: function (data) {
                if(data) {
                    $('#user_description_' + user_id).remove();
                    $(data).appendTo(_this).show('100');
                }
            }
        });
    });

    $('body').on('mouseleave', '.user-description-box', function(event) {
        var user_id = $(this).attr('data-user-id');
        $('#user_description_' + user_id).remove();
    });

});
