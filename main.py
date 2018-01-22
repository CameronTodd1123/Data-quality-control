#!/usr/bin/env python
#TODO change all += of lists to .append()
import clientdata
import datalags
import month_review

def main():
    print("it is running")
    dexibit_customers = clientdata.get_dexibit_cust_info()
    venue_errors = {}
    for venue_id in dexibit_customers:
        venue_errors[venue_id] = [datalags.check_lags_per_client(venue_id, dexibit_customers[venue_id])]
        venue_errors[venue_id].append(month_review.check_month_data_gaps_per_client(venue_id, dexibit_customers[venue_id]))

    #print(dexibit_customers)
    print(venue_errors)
    return

main()
