import clientdata
import datalags
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

#This file will hold all functions similar to datalags but will check 40 days worth of data and be checking for data gaps
#and outliers. Will have to look at some statistical packages that are already built to spot outliers in timeseries
#Also import and use Jupyter package like R to review data easier (Nani uses it)

def check_month_data_gaps_per_client(venue_id, client_integrations):
    month_data_gaps = []
    days_to_test = 40
    #venue_id = 8053450 #This is Antarctica test account with patchy data
    for integration in client_integrations:

        if integration == 'facebook':
            fb_gaps = check_facebook_data(venue_id, days_to_test)
            if fb_gaps != None:
                month_data_gaps.append(['facebook data gaps',fb_gaps])

        elif integration == 'instagram':
            inst_gaps = check_instagram_data(venue_id, days_to_test)
            if inst_gaps != None:
                month_data_gaps.append(['instagram data gaps',inst_gaps])

        elif integration == 'twitter':
            twitter_gaps = check_twitter_data(venue_id, days_to_test)
            if twitter_gaps != None:
                month_data_gaps.append(['twitter data gaps', twitter_gaps])

        elif integration == 'google_analytics':
            ga_gaps = check_google_analytics_data(venue_id,days_to_test)
            if ga_gaps != None:
                month_data_gaps.append(['google analytics data gaps', ga_gaps])



    return month_data_gaps

def check_facebook_data(venue_id,days):
    psql = """SELECT followers, record_date 
                        FROM social_media_followers 
                        WHERE venue_id = {} AND platform = 'Facebook'
                        ORDER BY record_date DESC 
                        LIMIT {}""".format(venue_id,days)
    venue_fb_data = clientdata._get_db_data(psql)
    facebook_date_gaps = check_missing_day_data_gap(venue_fb_data, days,datalags.facebook_lag)
    if facebook_date_gaps == None:
        return None
    else:
        return (facebook_date_gaps)


def check_instagram_data(venue_id,days):
    psql = """SELECT followers, record_date 
                        FROM social_media_followers 
                        WHERE venue_id = {} AND platform = 'Instagram'
                        ORDER BY record_date DESC 
                        LIMIT {}""".format(venue_id,days)
    venue_instagram_data = clientdata._get_db_data(psql)
    instagram_date_gaps = check_missing_day_data_gap(venue_instagram_data, days,datalags.instagram_lag)
    if instagram_date_gaps == None:
        return None
    else:
        return (instagram_date_gaps)


def check_twitter_data(venue_id,days):
    psql = """SELECT followers, record_date 
                        FROM social_media_followers 
                        WHERE venue_id = {} AND platform = 'Twitter'
                        ORDER BY record_date DESC 
                        LIMIT {}""".format(venue_id,days)
    venue_twitter_data = clientdata._get_db_data(psql)
    twitter_date_gaps = check_missing_day_data_gap(venue_twitter_data, days,datalags.facebook_lag)
    if twitter_date_gaps == None:
        return None
    else:
        return (twitter_date_gaps)

def check_google_analytics_data(venue_id,days):
    psql = """SELECT sessions, record_date
                        FROM google_analytics_daily 
                        WHERE venue_id = {} 
                        ORDER BY record_date DESC 
                        LIMIT {}""".format(venue_id,days)
    venue_ga_data = clientdata._get_db_data(psql)
    ga_date_gaps = check_missing_day_data_gap(venue_ga_data, days,datalags.google_analytics_lag)
    if ga_date_gaps == None:
        return None
    else:
        return (ga_date_gaps)





def check_missing_day_data_gap(venue_data, days_to_test,lag):
    data_gaps_dates = []
    if len(venue_data) == 0:
        data_gaps_dates.append('No Integration')
        return data_gaps_dates

    present_date = datetime.now().date()
    expected_day = max(present_date - timedelta(days=lag),venue_data[0][1].date())
    last_day_to_test = max(present_date - timedelta(days=lag) - timedelta(days=days_to_test),
                           venue_data[0][1].date() - timedelta(days=days_to_test))

    if venue_data[0][1].date() < last_day_to_test:
        data_gaps_dates.append('No relevant data')

    else:
        for actual_day in venue_data:
            value = actual_day[0]
            date_object = actual_day[1]
            if date_object.date() < last_day_to_test:
                break

            if value == None:
                data_gaps_dates.append(str(expected_day))

            if date_object.date() != expected_day:
                while date_object.date() != expected_day:
                    data_gaps_dates.append(str(expected_day))
                    expected_day = expected_day - timedelta(days=1)
                    if expected_day < last_day_to_test:
                        break
                expected_day = expected_day - timedelta(days=1)
            else:
                expected_day = expected_day - timedelta(days=1)

    if len(data_gaps_dates) == 0:
        return None
    else:
        return data_gaps_dates



def check_data_for_outliers(venue_data, sample_size):
    #We could use cooks distance, empirical rule: cooks distance > 4*mean(vector of all cooks distance) may be considered influential.'
    return