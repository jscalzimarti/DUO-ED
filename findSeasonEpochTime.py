import datetime
import time

season_data = [
    [1, 1278993600, 1314072000],  # Unix timestamps in milliseconds
    [1.5, 1314072001, 1322542799],
    [2, 1322542800, 1352696400],
    [2.5, 1352696401, 1359694799],
    [3, 1359694800, 1384146000],
    [3.5, 1384146001, 1389329999],
    [4, 1389330000, 1415682000],
    [4.5, 1415682001, 1421816399],
    [5, 1421816400, 1447218000],
    [5.5, 1447218001, 1453265999],
    [6, 1453266000, 1478581200],
    [6.5, 1478581201, 1481173199],
    [7, 1481173200, 1510030800],
    [7.5, 1510030801, 1516078799],
    [8, 1516078800, 1541998800],
    [8.5, 1541998801, 1548219599],
    [9, 1548219600, 1574139600],
    [9.5, 1574139601, 1578632399],
    [10, 1578632400, 1604984400],
    [10.5, 1604984401, 1610081999],
    [11, 1610082000, 1636952400],
    [11.5, 1636952401, 1641531599],
    [12, 1641531600, 1668402000],
    [12.5, 1668402001, 1673413199],
    [13, 1673413200, int(time.time())]
]

def find_season_epoch_time(currentSeason):
    for season in season_data:
        if season[0] == currentSeason:
            return season[1], season[2]
    
    # If the timestamp is after the last season, return the last season's name
    #if unix_timestamp_ms > season_data[-1][2]:
        #return season_data[-1][0]
        



def unix_milliseconds_to_date(unix_timestamp_ms):
    unix_timestamp_s = unix_timestamp_ms / 1000.0
    converted_datetime = datetime.datetime.fromtimestamp(unix_timestamp_s)
    return converted_datetime.date()