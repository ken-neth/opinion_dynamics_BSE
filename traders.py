# an Order/quote has a trader id, a type (buy/sell) price, quantity, timestamp, and unique i.d.
class Order:

        def __init__(self, tid, otype, price, qty, time, qid):
                self.tid = tid      # trader i.d.
                self.otype = otype  # order type
                self.price = price  # price
                self.qty = qty      # quantity
                self.time = time    # timestamp
                self.qid = qid      # quote i.d. (unique to each quote)

        def __str__(self):
                return '[%s %s P=%03d Q=%s T=%5.2f QID:%d]' % \
                       (self.tid, self.otype, self.price, self.qty, self.time, self.qid)

##################--Traders below here--#############
import random

# Trader superclass
# all Traders have a trader id, bank balance, blotter, and list of orders to execute
class Trader:

        def __init__(self, ttype, tid, balance, time, opinion, uncertainty, lower_op_bound, upper_op_bound, start_opinion):
                self.ttype = ttype      # what type / strategy this trader is
                self.tid = tid          # trader unique ID code
                self.balance = balance  # money in the bank
                self.blotter = []       # record of trades executed
                self.orders = []        # customer orders currently being worked (fixed at 1)
                self.n_quotes = 0       # number of quotes live on LOB
                self.willing = 1        # used in ZIP etc
                self.able = 1           # used in ZIP etc
                self.birthtime = time   # used when calculating age of a trader/strategy
                self.profitpertime = 0  # profit per unit time
                self.n_trades = 0       # how many trades has this trader done?
                self.lastquote = None   # record of what its last quote was

                self.opinion = opinion        # opinion between [0,1]
                self.uncertainty = uncertainty # uncertainty between [0, 2]

                self.lower_op_bound = lower_op_bound
                self.upper_op_bound = upper_op_bound
                self.lower_un_bound = 0
                self.upper_un_bound = 2

                self.start_opinion = start_opinion
                self.n_iter = 0


        def __str__(self):
                return '[TID %s type %s balance %s blotter %s orders %s n_trades %s profitpertime %s]' \
                       % (self.tid, self.ttype, self.balance, self.blotter, self.orders, self.n_trades, self.profitpertime)


        def add_order(self, order, verbose):
                # in this version, trader has at most one order,
                # if allow more than one, this needs to be self.orders.append(order)
                if self.n_quotes > 0 :
                    # this trader has a live quote on the LOB, from a previous customer order
                    # need response to signal cancellation/withdrawal of that quote
                    response = 'LOB_Cancel'
                else:
                    response = 'Proceed'
                self.orders = [order]
                if verbose : print('add_order < response=%s' % response)
                return response


        def del_order(self, order):
                # this is lazy: assumes each trader has only one customer order with quantity=1, so deleting sole order
                # CHANGE TO DELETE THE HEAD OF THE LIST AND KEEP THE TAIL
                self.orders = []


        def bookkeep(self, trade, order, verbose, time):

                outstr=""
                for order in self.orders: outstr = outstr + str(order)

                self.blotter.append(trade)  # add trade record to trader's blotter
                # NB What follows is **LAZY** -- assumes all orders are quantity=1
                transactionprice = trade['price']
                if self.orders[0].otype == 'Bid':
                        profit = self.orders[0].price - transactionprice
                else:
                        profit = transactionprice - self.orders[0].price
                self.balance += profit
                self.n_trades += 1
                self.profitpertime = self.balance/(time - self.birthtime)

                if profit < 0 :
                        print profit
                        print trade
                        print order
                        sys.exit()

                if verbose: print('%s profit=%d balance=%d profit/time=%d' % (outstr, profit, self.balance, self.profitpertime))
                self.del_order(order)  # delete the order


        # specify how trader responds to events in the market
        # this is a null action, expect it to be overloaded by specific algos
        def respond(self, time, lob, trade, verbose):
                return None

        # specify how trader mutates its parameter values
        # this is a null action, expect it to be overloaded by specific algos
        def mutate(self, time, lob, trade, verbose):
                return None

        def set_opinion(self, updated_opinion):

            validated_update = updated_opinion

            if updated_opinion >= self.upper_op_bound:
                # set to upper bound
                validated_update = self.upper_op_bound
            elif updated_opinion <= self.lower_op_bound:
                # set to lower bound
                validated_update = self.lower_op_bound

            self.opinion = validated_update

        def set_uncertainty(self, updated_uncertainty):

            validated_update = updated_uncertainty

            if updated_uncertainty >= self.upper_un_bound:
                # set to upper bound
                validated_update = self.upper_un_bound
            elif updated_uncertainty <= self.lower_un_bound:
                # set to lower bound
                validated_update = self.lower_un_bound

            self.uncertainty = validated_update


# Trader subclass Giveaway
# even dumber than a ZI-U: just give the deal away
# (but never makes a loss)
class Trader_Giveaway(Trader):

        def getorder(self, time, countdown, lob):
                if len(self.orders) < 1:
                        order = None
                else:
                        quoteprice = self.orders[0].price
                        order = Order(self.tid,
                                    self.orders[0].otype,
                                    quoteprice,
                                    self.orders[0].qty,
                                    time, lob['QID'])
                        self.lastquote=order
                return order



# Trader subclass ZI-C
# After Gode & Sunder 1993
class Trader_ZIC(Trader):

        def getorder(self, time, countdown, lob):
                if len(self.orders) < 1:
                        # no orders: return NULL
                        order = None
                else:
                        minprice = lob['bids']['worst']
                        maxprice = lob['asks']['worst']
                        qid = lob['QID']
                        limit = self.orders[0].price
                        otype = self.orders[0].otype
                        if otype == 'Bid':
                                quoteprice = random.randint(minprice, limit)
                        else:
                                quoteprice = random.randint(limit, maxprice)
                                # NB should check it == 'Ask' and barf if not
                        order = Order(self.tid, otype, quoteprice, self.orders[0].qty, time, qid)
                        self.lastquote = order
                return order


class Trader_opinionated_ZIC(Trader):

        def getorder(self, time, countdown, lob):

                if len(self.orders) < 1:
                        # no orders: return NULL
                        order = None
                else:
                        minprice = lob['bids']['worst']
                        maxprice = lob['asks']['worst']
                        qid = lob['QID']
                        limit = self.orders[0].price
                        otype = self.orders[0].otype

                        # get own opinion
                        opinion = self.opinion

                        if otype == 'Bid':
                                if opinion > 0.8: # price will go up so bid up to maxprice
                                    limit = maxprice
                                elif opinion < -0.8: # price will go down so only bid minprice
                                    limit = minprice
                                quoteprice = random.randint(minprice, limit)
                        else:
                                if opinion > 0.8: # price will go up so only accept maxprice
                                    limit = maxprice
                                elif opinion < -0.8: # price will go down so accept all bids
                                    limit = minprice
                                quoteprice = random.randint(limit, maxprice)
                                # NB should check it == 'Ask' and barf if not
                        order = Order(self.tid, otype, quoteprice, self.orders[0].qty, time, qid)
                        self.lastquote = order
                return order


# Trader subclass Shaver
# shaves a penny off the best price
# if there is no best price, creates "stub quote" at system max/min
class Trader_Shaver(Trader):

        def getorder(self, time, countdown, lob):
                if len(self.orders) < 1:
                        order = None
                else:
                        limitprice = self.orders[0].price
                        otype = self.orders[0].otype
                        if otype == 'Bid':
                                if lob['bids']['n'] > 0:
                                        quoteprice = lob['bids']['best'] + 1
                                        if quoteprice > limitprice :
                                                quoteprice = limitprice
                                else:
                                        quoteprice = lob['bids']['worst']
                        else:
                                if lob['asks']['n'] > 0:
                                        quoteprice = lob['asks']['best'] - 1
                                        if quoteprice < limitprice:
                                                quoteprice = limitprice
                                else:
                                        quoteprice = lob['asks']['worst']
                        order = Order(self.tid, otype, quoteprice, self.orders[0].qty, time, lob['QID'])
                        self.lastquote = order
                return order


# Trader subclass Sniper
# Based on Shaver,
# "lurks" until time remaining < threshold% of the trading session
# then gets increasing aggressive, increasing "shave thickness" as time runs out
class Trader_Sniper(Trader):

        def getorder(self, time, countdown, lob):
                lurk_threshold = 0.2
                shavegrowthrate = 3
                shave = int(1.0 / (0.01 + countdown / (shavegrowthrate * lurk_threshold)))
                if (len(self.orders) < 1) or (countdown > lurk_threshold):
                        order = None
                else:
                        limitprice = self.orders[0].price
                        otype = self.orders[0].otype

                        if otype == 'Bid':
                                if lob['bids']['n'] > 0:
                                        quoteprice = lob['bids']['best'] + shave
                                        if quoteprice > limitprice :
                                                quoteprice = limitprice
                                else:
                                        quoteprice = lob['bids']['worst']
                        else:
                                if lob['asks']['n'] > 0:
                                        quoteprice = lob['asks']['best'] - shave
                                        if quoteprice < limitprice:
                                                quoteprice = limitprice
                                else:
                                        quoteprice = lob['asks']['worst']
                        order = Order(self.tid, otype, quoteprice, self.orders[0].qty, time, lob['QID'])
                        self.lastquote = order
                return order




# Trader subclass ZIP
# After Cliff 1997
# NOTE: Kenny change init to suit opinion dynamics models
class Trader_ZIP(Trader):

        # ZIP init key param-values are those used in Cliff's 1997 original HP Labs tech report
        # NB this implementation keeps separate margin values for buying & selling,
        #    so a single trader can both buy AND sell
        #    -- in the original, traders were either buyers OR sellers

        def __init__(self, ttype, tid, balance, time, opinion, uncertainty):
                self.ttype = ttype
                self.tid = tid
                self.balance = balance
                self.birthtime = time
                self.profitpertime = 0
                self.n_trades = 0
                self.blotter = []
                self.orders = []
                self.n_quotes = 0
                self.lastquote = None
                self.job = None  # this gets switched to 'Bid' or 'Ask' depending on order-type
                self.active = False  # gets switched to True while actively working an order
                self.prev_change = 0  # this was called last_d in Cliff'97
                self.beta = 0.1 + 0.4 * random.random()
                self.momntm = 0.1 * random.random()
                self.ca = 0.05  # self.ca & .cr were hard-coded in '97 but parameterised later
                self.cr = 0.05
                self.margin = None  # this was called profit in Cliff'97
                self.margin_buy = -1.0 * (0.05 + 0.3 * random.random())
                self.margin_sell = 0.05 + 0.3 * random.random()
                self.price = None
                self.limit = None
                # memory of best price & quantity of best bid and ask, on LOB on previous update
                self.prev_best_bid_p = None
                self.prev_best_bid_q = None
                self.prev_best_ask_p = None
                self.prev_best_ask_q = None

                self.opinion = opinion
                self.uncertainty = uncertainty


        def getorder(self, time, countdown, lob):
                if len(self.orders) < 1:
                        self.active = False
                        order = None
                else:
                        self.active = True
                        self.limit = self.orders[0].price
                        self.job = self.orders[0].otype
                        if self.job == 'Bid':
                                # currently a buyer (working a bid order)
                                self.margin = self.margin_buy
                        else:
                                # currently a seller (working a sell order)
                                self.margin = self.margin_sell
                        quoteprice = int(self.limit * (1 + self.margin))
                        self.price = quoteprice

                        order = Order(self.tid, self.job, quoteprice, self.orders[0].qty, time, lob['QID'])
                        self.lastquote = order
                return order


        # update margin on basis of what happened in market
        def respond(self, time, lob, trade, verbose):
                # ZIP trader responds to market events, altering its margin
                # does this whether it currently has an order to work or not

                def target_up(price):
                        # generate a higher target price by randomly perturbing given price
                        ptrb_abs = self.ca * random.random()  # absolute shift
                        ptrb_rel = price * (1.0 + (self.cr * random.random()))  # relative shift
                        target = int(round(ptrb_rel + ptrb_abs, 0))
# #                        print('TargetUp: %d %d\n' % (price,target))
                        return(target)


                def target_down(price):
                        # generate a lower target price by randomly perturbing given price
                        ptrb_abs = self.ca * random.random()  # absolute shift
                        ptrb_rel = price * (1.0 - (self.cr * random.random()))  # relative shift
                        target = int(round(ptrb_rel - ptrb_abs, 0))
# #                        print('TargetDn: %d %d\n' % (price,target))
                        return(target)


                def willing_to_trade(price):
                        # am I willing to trade at this price?
                        willing = False
                        if self.job == 'Bid' and self.active and self.price >= price:
                                willing = True
                        if self.job == 'Ask' and self.active and self.price <= price:
                                willing = True
                        return willing


                def profit_alter(price):
                        oldprice = self.price
                        diff = price - oldprice
                        change = ((1.0 - self.momntm) * (self.beta * diff)) + (self.momntm * self.prev_change)
                        self.prev_change = change
                        newmargin = ((self.price + change) / self.limit) - 1.0

                        if self.job == 'Bid':
                                if newmargin < 0.0 :
                                        self.margin_buy = newmargin
                                        self.margin = newmargin
                        else :
                                if newmargin > 0.0 :
                                        self.margin_sell = newmargin
                                        self.margin = newmargin

                        # set the price from limit and profit-margin
                        self.price = int(round(self.limit * (1.0 + self.margin), 0))
# #                        print('old=%d diff=%d change=%d price = %d\n' % (oldprice, diff, change, self.price))


                # what, if anything, has happened on the bid LOB?
                bid_improved = False
                bid_hit = False
                lob_best_bid_p = lob['bids']['best']
                lob_best_bid_q = None
                if lob_best_bid_p != None:
                        # non-empty bid LOB
                        lob_best_bid_q = lob['bids']['lob'][-1][1]
                        if self.prev_best_bid_p < lob_best_bid_p :
                                # best bid has improved
                                # NB doesn't check if the improvement was by self
                                bid_improved = True
                        elif trade != None and ((self.prev_best_bid_p > lob_best_bid_p) or ((self.prev_best_bid_p == lob_best_bid_p) and (self.prev_best_bid_q > lob_best_bid_q))):
                                # previous best bid was hit
                                bid_hit = True
                elif self.prev_best_bid_p != None:
                        # the bid LOB has been emptied: was it cancelled or hit?
                        last_tape_item = lob['tape'][-1]
                        if last_tape_item['type'] == 'Cancel' :
                                bid_hit = False
                        else:
                                bid_hit = True

                # what, if anything, has happened on the ask LOB?
                ask_improved = False
                ask_lifted = False
                lob_best_ask_p = lob['asks']['best']
                lob_best_ask_q = None
                if lob_best_ask_p != None:
                        # non-empty ask LOB
                        lob_best_ask_q = lob['asks']['lob'][0][1]
                        if self.prev_best_ask_p > lob_best_ask_p :
                                # best ask has improved -- NB doesn't check if the improvement was by self
                                ask_improved = True
                        elif trade != None and ((self.prev_best_ask_p < lob_best_ask_p) or ((self.prev_best_ask_p == lob_best_ask_p) and (self.prev_best_ask_q > lob_best_ask_q))):
                                # trade happened and best ask price has got worse, or stayed same but quantity reduced -- assume previous best ask was lifted
                                ask_lifted = True
                elif self.prev_best_ask_p != None:
                        # the ask LOB is empty now but was not previously: canceled or lifted?
                        last_tape_item = lob['tape'][-1]
                        if last_tape_item['type'] == 'Cancel' :
                                ask_lifted = False
                        else:
                                ask_lifted = True


                if verbose and (bid_improved or bid_hit or ask_improved or ask_lifted):
                        print ('B_improved', bid_improved, 'B_hit', bid_hit, 'A_improved', ask_improved, 'A_lifted', ask_lifted)


                deal = bid_hit or ask_lifted

                if self.job == 'Ask':
                        # seller
                        if deal :
                                tradeprice = trade['price']
                                if self.price <= tradeprice:
                                        # could sell for more? raise margin
                                        target_price = target_up(tradeprice)
                                        profit_alter(target_price)
                                elif ask_lifted and self.active and not willing_to_trade(tradeprice):
                                        # wouldnt have got this deal, still working order, so reduce margin
                                        target_price = target_down(tradeprice)
                                        profit_alter(target_price)
                        else:
                                # no deal: aim for a target price higher than best bid
                                if ask_improved and self.price > lob_best_ask_p:
                                        if lob_best_bid_p != None:
                                                target_price = target_up(lob_best_bid_p)
                                        else:
                                                target_price = lob['asks']['worst']  # stub quote
                                        profit_alter(target_price)

                if self.job == 'Bid':
                        # buyer
                        if deal :
                                tradeprice = trade['price']
                                if self.price >= tradeprice:
                                        # could buy for less? raise margin (i.e. cut the price)
                                        target_price = target_down(tradeprice)
                                        profit_alter(target_price)
                                elif bid_hit and self.active and not willing_to_trade(tradeprice):
                                        # wouldnt have got this deal, still working order, so reduce margin
                                        target_price = target_up(tradeprice)
                                        profit_alter(target_price)
                        else:
                                # no deal: aim for target price lower than best ask
                                if bid_improved and self.price < lob_best_bid_p:
                                        if lob_best_ask_p != None:
                                                target_price = target_down(lob_best_ask_p)
                                        else:
                                                target_price = lob['bids']['worst']  # stub quote
                                        profit_alter(target_price)


                # remember the best LOB data ready for next response
                self.prev_best_bid_p = lob_best_bid_p
                self.prev_best_bid_q = lob_best_bid_q
                self.prev_best_ask_p = lob_best_ask_p
                self.prev_best_ask_q = lob_best_ask_q




##########################---trader-types have all been defined now--################
