import random
from traders import Order, Trader, Trader_Giveaway, Trader_Shaver, Trader_Sniper, Trader_ZIC, Trader_ZIP

def trader_type(robottype, name, min_Op, max_Op, model):
            opinion = 0.5
            uncertainty = 1.0
            if model == 'BC':
                opinion = random.uniform(min_Op, max_Op)
            elif model == 'RA':
                opinion = random.uniform(min_Op, max_Op)
                uncertainty = random.uniform(0, 2)
            elif model == 'RD':
                opinion = random.uniform(min_Op, max_Op)
                uncertainty = min((random.uniform(0.2, 2.0) + random.uniform(0, 1)), 2)
            else:
                sys.exit('FATAL: don\'t know that opinion dynamic model type %s\n' % model);

            if robottype == 'GVWY':
                    return Trader_Giveaway('GVWY', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op)
            elif robottype == 'ZIC':
                    return Trader_ZIC('ZIC', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op)
            elif robottype == 'SHVR':
                    return Trader_Shaver('SHVR', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op)
            elif robottype == 'SNPR':
                    return Trader_Sniper('SNPR', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op)
            elif robottype == 'ZIP':
                    return Trader_ZIP('ZIP', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op)
            else:
                    sys.exit('FATAL: don\'t know robot type %s\n' % robottype)


def shuffle_traders(ttype_char, n, traders):
        for swap in range(n):
                t1 = (n - 1) - swap
                t2 = random.randint(0, t1)
                t1name = '%c%02d' % (ttype_char, t1)
                t2name = '%c%02d' % (ttype_char, t2)
                traders[t1name].tid = t2name
                traders[t2name].tid = t1name
                temp = traders[t1name]
                traders[t1name] = traders[t2name]
                traders[t2name] = temp