auction_socket = io.connect('/auction');
$(document).ready(function() {
    /*
	$el = $('#description_box');
	var desc_pos = $el.offset(); // Store the position here so we can return the box once top is reach

	$(window).scroll(function(e){
		if( $(this).scrollTop() > desc_pos.top && $el.css('position') != 'fixed' ){
			$el.css({'position': 'fixed', 'top': '0px'});
		} else if ( $(this).scrollTop() < desc_pos.top && $el.css('position') == 'fixed')  {
			$el.css({'position': 'relative'});
		}
	});
	*/
	// var aucion_uri = '';
    var auction_pk = '';
	$('.fund').click(function() {
		// auction_uri = $(this).data('uri');
        auction_pk = $(this).data('pk');
	});
    auction_socket.on('AUTH_REQUIRED', function(url){
        redirect(url);
    });
    auction_socket.on('NOT_ENOUGH_CREDITS', function(url){
        redirect(url);
    });
    auction_socket.on('ALREADY_HIGHEST_BID', function(){
        alert('Already HighestBidder');
    });
    auction_socket.on('AUCTION_EXPIRED', function(){
       alert('Auction Expired');
    });
    auction_socket.on('auction_funded', function(auction_pk, amount_pleged, backers, funded){
        // item have been funded but not at full price yet
        var li = $("li#"+auction_pk);
        li.find('.bakers').text(backers);
        li.find('.amount_pleged').text('$' + amount_pleged);
        li.find('div.bar').attr('style', 'width: ' + funded + '%;').text(funded+"%");
        insert_notification(li.find('.fund-title a').text() + ' funded');
    });
    auction_socket.on('auction_fund_ended', function(auction_pk, time_left, html){
        // item have been funded for a full price so convert it to auction
        var block = $('li#'+auction_pk),
            next_id = block.prev().attr('id');
            html = $(html);
        html.insertAfter(block);
        block.slideUp('slow', function(){$(this).remove();});
        insert_notification(li.find('.fund-title a').text() + ' fund period ended');
    });
    auction_socket.on('auction_bid', function(auction_pk, time_left, username, avatar){
        // user made a bid on auction
        var block = $('li#'+auction_pk);
        block.find('img.social').attr('src', avatar).attr('title', username).show();
        block.find('span').text(username);
        block.reset_timer();
        insert_notification(username +' made a bid on' + block.find('.fund-title a').text());
    });

    var update_timers = function(){
        $('ul#items > li.showcase').each(function(){
            var self = $(this);
            var time_left = self.data('timeleft');
            if (time_left > 0) {

                self.data('timeleft', time_left-1);
                self.find('div.time').text(''+time_left -1 +' Seconds');
            } else{
                if (self.find('img.social').attr('src').length>0) {
                    // auction has a bid
                    var obj = {
                        self:self,
                        func: function(){
                            this.self.slideUp('slow');
                        }};
                    setTimeout(function(){ obj.func() }, 60000);
                    var panel = self.find('.fund-options');
                    if (!panel.find('span').length){
                        panel.find(".bid-btn").addClass('disabled');
                        $("<span>this auction has ended</span>").appendTo(panel);
                    }
                } else {
                    // no bid so far so reset timer
                    self.reset_timer();
                }
            }
        });
    };
    setInterval(update_timers, 1000);

	$('#fund_item').click(function(event) {
        event.preventDefault();
        var amount = $('input[name=option5]:checked', '#fund_form').attr('value');
        auction_socket.emit("fund", {amount:amount, auction_pk:auction_pk});
        $('#fundModal').modal('hide');
    });
    $('ul#items').on('click', '.bid-btn', function(event){
        var self = $(this);
        if (!self.hasClass('disabled')){
            auction_id = self.attr('data-auctionid');
            auction_socket.emit('bid', auction_id);
        }
        return false;
    });
	/* Quick sand sorting */
	// var $items_container = $('#items');
	// var $items_clone     = $items_container.clone(); // We sort this to do not break the original
	// var $sorting         = $('.btn-group.sorting button');
	// 	$sorting.click(function() {
	// 		console.log('sorting by name');
	// 		var $button = $(this);
	// 		var $filteredData = $items_clone.find('li'); // Get all the items

	// 		// Sort by name
	// 		var $sortedData = $filteredData.sorted({
	// 			by: function(v) {
 //                    return $(v).find('.fund-title').text().toLowerCase();
	// 			}
 //            });
	// 		console.log($sortedData);
 //            $items_container.quicksand($sortedData, {
 //                duration: 800,
 //                easing: 'easeInOutQuad'
 //            });

	// 	});

});

(function($) {
    $.fn.sorted = function(customOptions) {
        var options = {
            reversed: false,
            by: function(a) { return a.text(); }
        };
        $.extend(options, customOptions);
        $data = $(this);
        arr = $data.get();
        arr.sort(function(a, b) {
            var valA = options.by($(a));
            var valB = options.by($(b));
            if (options.reversed) {
                return (valA < valB) ? 1 : (valA > valB) ? -1 : 0;
            } else {
                return (valA < valB) ? -1 : (valA > valB) ? 1 : 0;
            }
        });
        return $(arr);
    };
    $.fn.reset_timer = function(){
        var self = $(this);
        self.data('timeleft', self.data('bidtime'));
    };
})(jQuery);

jQuery.fn.sortElements = (function(){

    var sort = [].sort;

    return function(comparator, getSortable) {

        getSortable = getSortable || function(){return this;};

        var placements = this.map(function(){

            var sortElement = getSortable.call(this),
                parentNode = sortElement.parentNode,

                // Since the element itself will change position, we have
                // to have some way of storing its original position in
                // the DOM. The easiest way is to have a 'flag' node:
                nextSibling = parentNode.insertBefore(
                    document.createTextNode(''),
                    sortElement.nextSibling
                );

            return function() {

                if (parentNode === this) {
                    throw new Error(
                        "You can't sort elements if any one is a descendant of another."
                    );
                }

                // Insert before flag:
                parentNode.insertBefore(this, nextSibling);
                // Remove flag:
                parentNode.removeChild(nextSibling);

            };

        });

        return sort.call(this, comparator).each(function(i){
            placements[i].call(getSortable.call(this));
        });

    };

})();
