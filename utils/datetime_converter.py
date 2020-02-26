from datetime import timezone, datetime, timedelta
import time


class DateTimeConverter:
    @classmethod
    def make_utc_datetime(cls, d):
        """Replaces tzinfo of datetime.datetime object to utc and adjusts datetime.
        If datetime object does not contain tzinfo, it will be considered as utc.
        """
        try:
            d = d - d.utcoffset()
        except TypeError:
            pass
        d = d.replace(tzinfo=timezone.utc)
        return d

    @classmethod
    def convert_datetime_to_unix_ts(cls, d):
        """Converts datetime.datetime object to unix timestamp in seconds.
        If datetime object does not contain tzinfo, it will be considered as utc."""
        d = cls.make_utc_datetime(d)
        return int(d.timestamp())

    @classmethod
    def convert_unix_ts_to_datetime(cls, ts):
        """Converts unix timestamp in seconds to datetime.datetime object with utc tzinfo."""
        d = datetime.fromtimestamp(ts)
        offset = time.timezone / 3600
        d = d + timedelta(hours=offset)
        d = cls.make_utc_datetime(d)
        return d
