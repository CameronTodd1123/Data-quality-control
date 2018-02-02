#!/usr/bin/env python

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

    print_results(venue_errors)



def print_results(venue_errors):
    for venue_id, errors in venue_errors.items():
        data_lags = errors[0]
        data_gaps = errors[1]
        if data_lags != None:
            for integration_lag in data_lags:
                print("{} has lag in {} data".format(venue_id,integration_lag))

        if data_gaps != None:
            for integration_gap in data_gaps:
                string_of_missing_days = ", ".join(integration_gap[1])
                print("{} has missing {} data: {}".format(venue_id,integration_gap[0], string_of_missing_days))






    return

main()
