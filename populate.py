import random
from traders import Order, Trader, Trader_Giveaway, Trader_Shaver, Trader_Sniper, Trader_ZIC, Trader_ZIP, Trader_opinionated_ZIC, Trader_Bubble_ZIC, Trader_opinionated_near_ZIC

def trader_type(robottype, name, min_Op, max_Op, u_min, u_max, model, start_opinion, extreme_distance):
            opinion = 0.5
            uncertainty = 1.0
            if model == 'BC':
                opinion = random.uniform(min_Op+extreme_distance, max_Op-extreme_distance)
            elif model == 'RA':
                opinion = random.uniform(min_Op+extreme_distance, max_Op-extreme_distance)
                uncertainty = random.uniform(u_min, u_max)
            elif model == 'RD':
                opinion = random.uniform(min_Op+extreme_distance, max_Op-extreme_distance)
                uncertainty = random.uniform(u_min, u_max)
                # uncertainty = min((random.uniform(0.2, 2.0) + random.uniform(0, 1)), 2)
            else:
                sys.exit('FATAL: don\'t know that opinion dynamic model type %s\n' % model);

            if robottype == 'GVWY':
                    return Trader_Giveaway('GVWY', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'ZIC':
                    return Trader_ZIC('ZIC', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'SHVR':
                    return Trader_Shaver('SHVR', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'SNPR':
                    return Trader_Sniper('SNPR', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'ZIP':
                    return Trader_ZIP('ZIP', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'O-ZIC':
                    return Trader_opinionated_ZIC('O-ZIC', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'B-ZIC':
                    return Trader_Bubble_ZIC('B-ZIC', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
            elif robottype == 'ON-ZIC':
                    return Trader_opinionated_near_ZIC('ON-ZIC', name, 0.00, 0, opinion, uncertainty, min_Op, max_Op, start_opinion)
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
