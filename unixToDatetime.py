import datetime

def unix_milliseconds_to_datetime(unix_timestamp_ms):
    try:
        unix_timestamp_s = unix_timestamp_ms / 1000.0
        converted_datetime = datetime.datetime.fromtimestamp(unix_timestamp_s)
        return converted_datetime
    except OSError as e:
        print("Error:", e)
        return None

# Example usage
unix_timestamp_ms = 1692256097504  # Replace with your Unix timestamp in milliseconds
converted_datetime = unix_milliseconds_to_datetime(unix_timestamp_ms)

if converted_datetime:
    print("Unix Timestamp (milliseconds):", unix_timestamp_ms)
    print("Converted Datetime:", converted_datetime)
