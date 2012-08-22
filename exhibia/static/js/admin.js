var getKeys = function(obj){
    var keys = [];
    for(var key in obj){
        keys.push(key);
    }
    return keys;
}

var unit_plural = function(n){
    return n==1?"":"s";
}

var get_time = function(seconds){
    if (isNaN(seconds)) {
        return seconds;
    } else if (seconds >=1 ) {
        hour = Math.floor(seconds / 3600);
        if (hour < 10)
            hour = "0" + hour;
        min = Math.floor((seconds - hour*3600) / 60);
        if (min < 10)
            min = "0"  + min;
        sec = seconds % 60;
        if (sec < 10)
            sec = "0" + sec;
        timeString = "";
        return timeString + hour + ":" + min + ":" + sec;
        if (hour)
            timeString += hour + "<span class=\"time_text\"> Hour" + unit_plural(hour) + " </span>";
        if (min)
            timeString += min + "<span class=\"time_text\"> Minute" + unit_plural(min) + " </span>";
        if (sec)
            timeString += sec + "<span class=\"time_text\"> Second" + unit_plural(sec) + " </span>";
        return timeString;
    } else {
        return "--:--:--";
    }
}

function minus(a, b){
    result = [];
    for (i=0; i < a.length; ++i){
        e = a[i];
        if ($.inArray(e, b)==-1){
            result.push(e);
        }
    }
    return result;
}

function get_real_keys(items){
    result = [];
    for (i in items){
        result.push(items[i].id);
    };
    return result;
}
function Auctions(info){
    this.auctions = info;
    this.get_ids =  function(){
        return getKeys(this.auctions);
    };

    this.ids = function(){
        return get_real_keys(this.auctions);
    }
}

function Items(info){
    this.items = info;
    this.get_ids =  function(){
        return getKeys(this.items);
    };
    this.ids = function(){
        return get_real_keys(this.items);
    }
}


function get_all_ids(){
    result = [];
    result = result.concat($.exhibia['auctions'].ids());
    if ($.exhibia['items']){
        return result.concat($.exhibia['items'].ids());
    }
    return result;
}
function update_auctions_ui(auctions){
    for(a_id in auctions){
        auction = auctions[a_id];
        // Update Seconds left
        if (auction.status == "p" || auction.status=="w") {
            $('#timer_' + auction['id']).html(get_time(auction['time_left']));
        } else if(auction.status == "s"){
            $('#timer_' + auction['id']).text("Auctions will resume shortly.");
        } else if (auction.status == 'e' || auction.status == 'f'){
            $('#timer_' + auction['id']).text("This auction has ended");
        }
        // Update Bidding time
        $('#bidding_time_' + auction.id).html(get_time(auction.bidding_time));
        if (auction.last_bidder == ''){
            $('#last_bidder_' + auction.id).html("Be the first bidder");
        }else{
            $('#last_bidder_' + auction.id).html(auction.last_bidder);
        }
        if (auction.last_bidder_img){
            console.log(auction.last_bidder_img);
            $('#last_bidder_img_' + auction.id).attr('src', auction.last_bidder_img)
        }

    }
}

function admin_update_auctions_ui(auctions){
    for(a_id in auctions){
        auction = auctions[a_id];
        // Update Seconds left
        if (auction.status == "p" || auction.status=="w") {
            $('#timer_' + auction['id']).html(get_time(auction['time_left']));
            $('#status_' + auction.id).attr('checked', 'checked');
        } else if(auction.status == "s"){
            $('#timer_' + auction['id']).text("Auctions will resume shortly.");
            $('#status_' + auction.id).removeAttr("checked");
        } else if (auction.status == 'e' || auction.status == 'f'){
            $('#timer_' + auction['id']).text("This auction has ended");
        }
        // Update Bidding time
        $('#bidding_time_' + auction.id).html(get_time(auction.bidding_time));
        if (auction.last_bidder != ''){
            $('#last_bidder_' + auction.id).html(auction.last_bidder);
        }
        if (auction.last_bidder_img){
            $('#last_bidder_img_' + auction.id).attr('src', auction.last_bidder_img)
        }
        $('#funded_' + auction.id).html(auction.funded);
        $('#backers_' + auction.id).html(auction.backers);
    }
}

function add_remove_auctions(){
    all_items_ui_ids = $.map($('.item'), function(value,i){ return parseInt($(value).attr('data-id')) });
    ids = get_all_ids()
    items_to_delete = minus(all_items_ui_ids, ids);
    items_to_add = minus(ids, all_items_ui_ids);
    for (i in items_to_delete){
        $('li[data-id=' + items_to_delete[i] +']').hide(2000, function(){
            $('li[data-id=' + items_to_delete[i] +']').remove();
        });
    }
    $.post('/items/get/', { items: items_to_add }, function(data){
        $('#items_container').append(data);
    });
}

function redirect(url){
    window.location.replace(url);
}
