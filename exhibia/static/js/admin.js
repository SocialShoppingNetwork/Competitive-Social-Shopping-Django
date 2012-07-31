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
        console.log(seconds);
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

function Auctions(info){
    this.auctions = info;
    this.get_ids =  function(){
        return getKeys(this.auctions);f
    };
    this.update_ui = function(info){
        this.auctions = info;
        for(a_id in this.auctions){
            auction = this.auctions[a_id];
            // Update Seconds left
            if (auction.status == "p" || auction.status=="w") {
                $('#timer_' + auction['id']).html(get_time(auction['time_left']));
            } else if(auction.status == "s"){
                $('#timer_' + auction['id']).text("Auctions will resume shortly.");
            } else if (auction.status == 'e' || auction.status == 'f'){
                $('#timer_' + auction['id']).text("This auction has ended");
            }
            $('#bidding_time_' + auction['id']).text(auction.bidding_time);
            // Update Bidding time
            //$('#bidding_time_' + auction.id).html(get_time(auction.bidding_time));
            if (auction.status == 'w'){
                $('#last_bidder_' + auction.id).html("Be the first bidder");
            }else{
                $('#last_bidder_' + auction.id).html(auction.last_bidder);
            }
            $('#current_price_' + auction.id).html(auction.current_price);

            //Matic Fields
            $('#bids_left_' + auction.id).html(auction.matic.bids_left);
            $('#usersbid_' + auction.id).html(auction.matic.users_bid);
            if (auction.matic.win){
                $('#win_' + auction.id).attr('checked', 'checked');
            }else{
                $('#win_' + auction.id).removeAttr("checked");
            }
            //console.log(auction.status);
            if (auction.status == 's'){
                $('#status_' + auction.id).removeAttr("checked");
            }else{
                $('#status_' + auction.id).attr('checked', 'checked');
            }
        }
    };
}

function redirect(url){
    window.location.replace(url);
}

