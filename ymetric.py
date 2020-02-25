# calc_y()
def calc_y(u, pe, extreme_distance, Max_Op, Min_Op, n_moderate, traders):

    # if(dump>0):
    #     # write population values to file on this run
    #     # filename=model_name+"_%2.3f"%u+"_%2.3f"%pe+"_%2d"%dumpid+'.csv'
    #     filename = "ymetric.csv"
    #     outfile=open(filename,'w')

    # now do the post-experiment analysis
    # compare current opinion and initial opinion
    p_prime_plus_count=0
    p_prime_minus_count=0

    for key in list(traders.keys()):
        trader = traders[key]
        # increment p_prime_plus_count if this is a moderate that went +ve extreme
        if((trader.start_opinion == "moderate")&((Max_Op-trader.opinion) <= extreme_distance)):
            p_prime_plus_count += 1
        # increment p_prime_minus_count if this is a moderate that went -ve extreme
        if((trader.start_opinion == "moderate")&((trader.opinion-Min_Op) <= extreme_distance)):
            p_prime_minus_count += 1

    p_prime_plus=p_prime_plus_count/float(n_moderate)
    p_prime_minus=p_prime_minus_count/float(n_moderate)

    y=(p_prime_plus*p_prime_plus)+(p_prime_minus*p_prime_minus)
    print("u=%f pe=%f y=%f" % (u, pe, y))


    # if(dump>0):
    #     outstr="\n"
    #     keys = list(traders.keys())
    #     outfile.write("%f \n" % y)
    #     #write the number of interactions each agent has had
    #     # for i in range(N):
    #     #     if(i<(n-1)):
    #     #         outstr+="%3d"%traders[keys[i]].n_iter+", "
    #     #     else:
    #     #         outstr+="%3d"%traders[keys[i]].n_iter+"\n"
    #     #         outfile.write(outstr)
    #
    #     outfile.close()

    return (u, pe, y)


def calc_y_stats(u,pe, ys, sims_per_point):
    y_max=-10.0
    y_min=10.0
    y_sum=0.0
    y_sumsq=0.0
    for y in ys:
        y_sum=y_sum+y
        y_sumsq=y_sumsq+(y*y)
        if(y>y_max):
            y_max=y
        if(y<y_min):
            y_min=y
    y_avg=y_sum/sims_per_point
    y_sd=sqrt((y_sumsq/sims_per_point)-(y_avg*y_avg))
    return (y_max, y_min, y_avg, y_sd)
