import clientdata
from datetime import datetime, timedelta
import clientdata
#TODO change all += of lists to .append()
#Variables to outline expected lag times in days
facebook_lag = 2
instagram_lag = 2
twitter_lag = 2
google_analytics_lag = 4
presence_lag_time = 2
weather_lag = 1



def check_lags_per_client(venue_id, client_integrations):
    venue_lags = []
    for integration in client_integrations:

        if integration == 'facebook':
            if check_facebook_followers_lag_test(venue_id) == True:
                venue_lags.append('facebook followers lag')
            if check_facebook_engagement_impressions_lag_test(venue_id) == True:
                venue_lags.append('facebook engagement-impressions lag')
            if check_facebook_reactions_lag_test(venue_id) == True:
                venue_lags.append('facebook reactions lag')

        elif integration == 'instagram':
            if check_instagram_lag_test(venue_id) == True:
                venue_lags.append('instagram lag')
        elif integration == 'twitter':
            if check_twitter_lag_test(venue_id) == True:
                venue_lags.append('twitter lag')
        elif integration == 'google_analytics':
            if check_google_analytics_lag_test(venue_id) == True:
                venue_lags.append('google analytics lag')
        elif integration == 'presence':
            if check_presence_lag_test(venue_id) == True:
                venue_lags.append('presence lag')
        elif integration == 'weather':
            if check_weather_lag_test(venue_id) == True:
                venue_lags.append('weather lag')

    return venue_lags



def check_facebook_followers_lag_test(venue_id):
    psql = """SELECT followers, record_date 
                    FROM social_media_followers 
                    WHERE venue_id = {} AND platform = 'Facebook'
                    ORDER BY record_date DESC 
                    LIMIT 1""".format(venue_id)
    venue_fb_data = clientdata._get_db_data(psql)
    if check_lag(venue_fb_data, facebook_lag) == True:
        return True
    else:
        return False

def check_facebook_engagement_impressions_lag_test(venue_id):
    psql = """SELECT postimpressions, fromdate 
                    FROM facebookpostinsightreading 
                    WHERE venue_id = {} 
                    ORDER BY fromdate DESC 
                    LIMIT 1""".format(venue_id)
    venue_fb_data = clientdata._get_db_data(psql)
    if check_lag(venue_fb_data, facebook_lag) == True:
        return True
    else:
        return False

def check_facebook_reactions_lag_test(venue_id):
    psql = """SELECT pageconsumptions, fromdate 
                    FROM facebookreading 
                    WHERE venue_id = {} 
                    ORDER BY fromdate DESC 
                    LIMIT 1""".format(venue_id)
    venue_fb_data = clientdata._get_db_data(psql)
    if check_lag(venue_fb_data, facebook_lag) == True:
        return True
    else:
        return False


def check_instagram_lag_test(venue_id):
    psql = """SELECT followers, record_date 
                    FROM social_media_followers 
                    WHERE venue_id = {} AND platform = 'Instagram'
                    ORDER BY record_date DESC 
                    LIMIT 1""".format(venue_id)
    venue_instagram_data = clientdata._get_db_data(psql)
    if check_lag(venue_instagram_data, instagram_lag) == True:
        return True
    else:
        return False

def check_twitter_lag_test(venue_id):
    psql = """SELECT twitterfollowers, date 
                    FROM analytics 
                    WHERE venue_id = {}
                    ORDER BY date DESC 
                    LIMIT 1""".format(venue_id)
    venue_twitter_data = clientdata._get_db_data(psql)
    if check_lag(venue_twitter_data, twitter_lag) == True:
        return True
    else:
        return False

def check_google_analytics_lag_test(venue_id):
    psql = """SELECT sessions, record_date 
                    FROM google_analytics_daily
                    WHERE venue_id = {}
                    ORDER BY record_date DESC 
                    LIMIT 1""".format(venue_id)
    venue_ga_data = clientdata._get_db_data(psql)
    if check_lag(venue_ga_data, google_analytics_lag) == True:
        return True
    else:
        return False


def check_presence_lag_test(venue_id):
    psql = """SELECT dwell_time,record_date 
                    FROM daily_presence_by_zone 
                    WHERE venue_id = {} 
                    ORDER BY record_date DESC 
                    LIMIT 1""".format(venue_id)
    venue_presence_data = clientdata._get_db_data(psql)

    present_date = datetime.now()
    if len(venue_presence_data) == 0:
        return True
    elif venue_presence_data[0][1] < present_date.date() - timedelta(days=presence_lag_time):
        return True
    else:
        return False


def check_weather_lag_test(venue_id):
    psql = """SELECT temperaturecelsius, timestamp 
                        FROM weatherdatareading
                        WHERE venue_id = {}
                        ORDER BY timestamp DESC 
                        LIMIT 1""".format(venue_id)
    venue_weather_data = clientdata._get_db_data(psql)
    if check_lag(venue_weather_data, weather_lag) == True:
        return True
    else:
        return False



def check_lag(client_data, suitable_lag):
    present_date = datetime.now()
    if len(client_data) == 0:
        return True
    elif client_data[0][1].date() < present_date.date() - timedelta(days=suitable_lag):
        return True
    else:
        return False



#Seems to be 3 types of admission data in different tables depending on what client chooses in settings
# Too hard for now will have to come back later  TODO later?
def check_foot_traffic_lag(venue_id):
    return


