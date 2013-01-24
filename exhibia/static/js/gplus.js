(function() {
    gplus_callback = function(){
        console.log('gplus_callback');
        if (window.user_is_logged=='True'){
                $.ajax({
                    url:'/socials/user_like/',
                    data: {
                        href:window.location.href,
                        type:'G',
                        source:'google-oauth2',
                        item:$('meta[name="id"]').attr('content')
                    }
                }, function(data){'hooray'+console.log(data)});
            }
    }
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = '//apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);

})();
