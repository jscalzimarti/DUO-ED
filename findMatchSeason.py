import datetime
import time

season_data = [
    [1, 1278993600000, 1314072000000],  # Unix timestamps in milliseconds
    [1.5, 1314072000001, 1322542799999],
    [2, 1322542800000, 1352696400000],
    [2.5, 1352696400001, 1359694799999],
    [3, 1359694800000, 1384146000000],
    [3.5, 1384146000001, 1389329999999],
    [4, 1389330000000, 1415682000000],
    [4.5, 1415682000001, 1421816399999],
    [5, 1421816400000, 1447218000000],
    [5.5, 1447218000001, 1453265999999],
    [6, 1453266000000, 1478581200000],
    [6.5, 1478581200001, 1481173199999],
    [7, 1481173200000, 1510030800000],
    [7.5, 1510030800001, 1516078799999],
    [8, 1516078800000, 1541998800000],
    [8.5, 1541998800001, 1548219599999],
    [9, 1548219600000, 1574139600000],
    [9.5, 1574139600001, 1578632399999],
    [10, 1578632400000, 1604984400000],
    [10.5, 1604984400001, 1610081999999],
    [11, 1610082000000, 1636952400000],
    [11.5, 1636952400001, 1641531599999],
    [12, 1641531600000, 1668402000000],
    [12.5, 1668402000001, 1673413199999],
    [13, 1673413200000, int(time.time() * 1000)]
]

def find_match_season(unix_timestamp_ms):
    for i in range(len(season_data)):
        start_timestamp = season_data[i][1]
        end_timestamp = season_data[i][2]
            
        if start_timestamp <= unix_timestamp_ms <= end_timestamp:
            season_name = season_data[i][0]
            return season_name
    
    # If the timestamp is after the last season, return the last season's name
    if unix_timestamp_ms > season_data[-1][2]:
        return season_data[-1][0]
        



def unix_milliseconds_to_date(unix_timestamp_ms):
    unix_timestamp_s = unix_timestamp_ms / 1000.0
    converted_datetime = datetime.datetime.fromtimestamp(unix_timestamp_s)
    return converted_datetime.date()
