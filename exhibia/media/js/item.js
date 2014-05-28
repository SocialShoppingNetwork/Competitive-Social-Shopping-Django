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
     function slotmachine(element, o, is_text_or_value) {
          var start_value = parseFloat(is_text_or_value ? element.text():element.val());
          $({someValue: start_value}).animate({someValue: o}, {
              duration: 1000,
              easing: 'swing',
              step: function () {
                  if(is_text_or_value){
                    element.text(this.someValue.toFixed(0));
                  }else{
                    element.val(this.someValue.toFixed(0));
                  }
              }
          });
      }


    var auction_pk = '';
	$('body').on('click', '.fund', function() {
		// auction_uri = $(this).data('uri');
        auction_pk = parseInt($(this).data('pk'));
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
    auction_socket.on('AUCTION_LOCKED', function(){
       alert('Auction was locked');
    });
    auction_socket.on('auction_funded', function(auction_pk, amount_pleged, backers, funded){
        // item have been funded but not at full price yet
        var div = $("div#auction-"+auction_pk);
        div.find('.bakers').text(backers);
        div.find('.progress-bar').attr('style', 'width: ' + funded + '%;');
        if(funded >= 100){
            funded = 99
        }
        slotmachine(div.find('.funded'), funded, true);
        insert_notification(div.find('.item-name h6').text() + ' has been funded');
    });
    auction_socket.on('auction_fund_ended', function(auction_pk, time_left, html){
        var div = $("div#auction-"+auction_pk);
        $(html).insertBefore($('#items li:first'));
        block.slideUp('slow', function(){$(this).remove();});
        insert_notification(block.find('.fund-title a').text() + ' has been opened for bidding');

        // item have been funded for a full price so convert it to auction
//        var block = $('li#'+auction_pk),
//            next_id = block.prev().attr('id');
//            html = $(html);
//        html.insertAfter(block);
//        block.slideUp('slow', function(){$(this).remove();});
//        insert_notification(block.find('.fund-title a').text() + ' has been opened for bidding');


    });
    auction_socket.on('auction_bid', function(auction_pk, time_left, username, avatar) {
        // user made a bid on auction

        var modal = $('#item_modal_'+ auction_pk);
        modal.find('.showcase-timer').show();
        modal.find('.showcase-timer').reset_timer();
        modal.find('.start-message').hide();
        // TODO insert new bidder photo to the list in the modal

        var block = $('#item_' + auction_pk);
        block.find('.item-bidder-foto').attr('src', avatar);
        block.find('.wrapper-foto').show();
        block.find('.item-last-bidder').text(username);
        block.find('.showcase-timer').show();
        block.find('.start-message').hide();
        block.find('.showcase-timer').reset_timer();
        insert_notification(username +' made a bid on ' + block.find('.item-name').text());
    });

    var update_timers = function() {
        $('body').find('.timer').each(function() {
            var self = $(this);
            var time_left = self.data('timeleft');
            if (time_left > 0) {
                if(self.is(':visible')) {
                    self.data('timeleft', time_left-1);
                    self.text(get_time(time_left -1));
                }
            } else {
                // auction has a bid
//                if (self.is(':visible')) {
                    if(self.hasClass('bid-refund-timer')){
                        self.closest('.thumbnail').remove();
                    }
                    if(self.hasClass('showcase-timer')){
                        var tr = self.closest('tr');
                        tr.empty();
                        tr.addClass('winner');
                        tr.append('<td><div class="txt">Winner</div></td>');
                        tr.closest('tbody').find('.item-timer').remove();
                    }
                    if(self.hasClass('win-limit-timer')){
                        self.closest('.panel-footer').remove();
                        // TODO send signal and revive those buttons that we need
                    }
//                }
//                else {
//                    self.reset_timer();
//                }
            }
        });
    };
    setInterval(update_timers, 1000);

    $('body').on('keyup', '#custom_value', function(event) {
        var amount = parseFloat($(this).val());

        if (isNaN(amount)) {
            amount = 0;
        }
        var full_amount = amount + amount * 0.2;

        slotmachine($('#total-bids'), full_amount, true);
        slotmachine($('#custom_bonus'), full_amount, true);
    });

    $('#is_custom_value').click(function() {
        if ($(this).prop('checked')) {
            $('#fund_form input[name=option5]:checked').prop('checked', false);
            var amount = parseFloat($('#custom_value').val());

            if (isNaN(amount)) {
                amount = 0;
            }

            amount += amount * 0.2;
            slotmachine($('#total-bids'), amount, true);

        }
    });

	$('body').on('click', '#fund_item', function(event) {
        event.preventDefault();
        var amount = 0;

        if ($('#is_custom_value').prop('checked')) {
            amount = parseFloat($('#custom_value').val());
            amount += amount * 0,2;
        }
        else {
            amount = $('input[name=option5]:checked', '#fund_form').attr('value');
        }

        if(!amount) {
            return;
        }
        auction_socket.emit("fund", {amount:amount, auction_pk:auction_pk});
        $('#ModalFund').modal('hide');
        $('#fund_form input[name=option5]').prop('checked', '');
        $('#total-bids').text(0);
    });

	$('body').on('click', '.btn-buy', function(event) {
        // initiate ajax call to get the right buy now form
        event.preventDefault();
        var id= $(this).data('id');
        var exists = $('#modal_buy_now_'+id).length;
        if(!exists){
            $.ajax({
                type: "POST",
                url: "/checkout/append_buy_now_form/",
                data: {'id': id },
                dataType: 'html',
                success: function (data) {
                    if(data) {
                        $('#ModalBuyNow').html(data);
                        $('#ModalBuyNow').modal('show');
                    }
                }
            });
        }else{
            $('#ModalBuyNow').modal('show');
        }
    });
    $('body').on('click', '.btn-battle', function(event) {
        // initiate ajax call to get the right buy now form
        event.preventDefault();
        var id= $(this).data('id');
        var exists = $('#item_modal_'+id).length;
        if(!exists){
            $.ajax({
                type: "POST",
                url: "/items/append_battle_modal/",
                data: {'id': id },
                dataType: 'html',
                success: function (data) {
                    if(data) {
                        $('#ModalBattleView').html(data);
                        $('#ModalBattleView').modal('show');
                    }
                }
            });
        }else{
            $('#ModalBattleView').modal('show');
        }


    });
    $('body').on('click', '.bid-btn', function(event){
        var self = $(this);
        if (!self.hasClass('disabled')){
            auction_id = self.attr('data-auctionid');
            auction_socket.emit('bid', auction_id);
        }
        return false;
    });
    $('#fund_form input[name="option5"]').on('click', function(event){
        $('#is_custom_value').prop('checked', false);
        var val = $(this).val();
        slotmachine($('#total-bids'), val, true);

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
