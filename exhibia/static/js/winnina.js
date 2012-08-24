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
    this.auctions = info;
    this.get_ids =  function(){
        return getKeys(this.auctions);
    };
    this.ids = function(){
        return get_real_keys(this.auctions);
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
        //$('#current_offer_' + auction.id).html(auction.current_offer);
    }
}

function update_items_ui(items){
    for(a_id in items){
        auction = items[a_id];
        $('#backers_' + auction.id).html(auction.backers);
    }
};

function add_remove_auctions(){
    all_items_ui_ids = $.map($('.item'), function(value,i){ return parseInt($(value).attr('data-id')) });
    ids = get_all_ids()

    items_to_delete = minus(all_items_ui_ids, ids);
    items_to_add = minus(ids, all_items_ui_ids);
    //console.log('TO DELETE');
    //console.log(items_to_delete);
    for (i in items_to_delete){
        $('li[data-id=' + items_to_delete[i] +']').hide(2000, function(){
            $('li[data-id=' + items_to_delete[i] +']').remove();
        });
    }
    //console.log('TO ADD');

    //console.log(items_to_add);
    //auctions_to_add = $.map(minus(auctions_ids, current_ids), function(value, i){ return value.substr(2); });
    $.post('/items/get/', { items: items_to_add }, function(data){
        $('#items_container').append(data);
        //console.log(data);
    });
}

function redirect(url){
    window.location.replace(url);
}

function update_bids(){
    $.get('/accounts/profile/bids/', function(data) {
        bids = data;
        $('#member_bids').text(bids);
    });
}

function get_account_bids(f){
    $.get('/accounts/profile/bids/', function(data) {
        f(data);
    });
}

function fill_payment_form(item_description, item_price, custom_value){
    $('#paynow_item_desc').attr('value', item_description);
    $('#paynow_item_price').attr('value', item_price);
    if (custom_value) $('#paynow_custom_field2').attr('value', custom_value);
}

function send_message(message){
    $.ajax({
        type: "POST",
        url: "/chat/send-message/",
        data: JSON.stringify({'message':message}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){alert(data);},
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
}


function ban_user(username){
    $.post("/chat/send-message/",{'username':username});
}