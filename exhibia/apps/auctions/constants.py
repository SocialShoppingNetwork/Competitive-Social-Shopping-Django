AUCTION_WAITING = 'w'
AUCTION_PROCESSING = 'p'
AUCTION_PAUSE = 's'
AUCTION_JUST_ENDED = 'e'
AUCTION_FINISHED = 'f'
AUCTION_WAITING_PAYMENT = 'm'
AUCTION_PAID = 'd'
AUCTION_COMPLETED = 'c'
# delay before displaying for bidding (after item was fully funded)
TRANSITION_PHASE_1 = 't1'
# item will stay there for 10 mins more displaying the winner until disappears from bidding and appears to funding
TRANSITION_PHASE_2 = 't2'

AUCTION_WAITING_PLEDGE = 'w'
AUCTION_FINISHED_NO_PLEDGED = 'x'
AUCTION_SHOWCASE = 'p'

BID_NORMAL = 'n'
BID_MATIC = 'm'


ORDER_WAITING_PAYMENT = 'wp'
ORDER_SHIPPING_FEE_REQUESTED = 'rf'
ORDER_PROCESSING_ORDER = 'rf'
ORDER_PAID = 'pd' # Processing Order
ORDER_DELIVERED = 'dl'
ORDER_WAITING_TESTIMONIAL = 'wt'
