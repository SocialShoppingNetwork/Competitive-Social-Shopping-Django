if (window.facebook_appId) {
    window.fbAsyncInit = function() {
        FB.init({
            appId: window.facebook_appId,
            status: true,
            cookie: true,
            xfbml: true,
            oauth: true
        });
        FB.Event.subscribe('edge.create', function(response) {
            if (window.user_is_logged=='True'){
                console.log('hoorai')
            }
        });
    };
    (function(d) {
        var js, id = 'facebook-jssdk';
        if (d.getElementById(id)) {
            return;
        }
        js = d.createElement('script');
        js.id = id;
        js.async = true;
        js.src = "//connect.facebook.net/en_US/all.js";
        d.getElementsByTagName('head')[0].appendChild(js);
    }(document));
}
