

def parse_timestamp(my_dt):
    """
    Param my_dt (datetime.datetime) like status.created_at
    Converts datetime to string, formatted for Google BigQuery as YYYY-MM-DD HH:MM[:SS[.SSSSSS]]
    """
    return my_dt.strftime("%Y-%m-%d %H:%M:%S")
