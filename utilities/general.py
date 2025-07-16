from datetime import datetime


class General:
    @staticmethod
    def parse_time(time_str):
        # Example: "00:01:23" -> 83 seconds
        parts = time_str.strip().split(":")
        parts = [int(p) for p in parts]
        if len(parts) == 3:
            h, m, s = parts
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = parts
            return m * 60 + s
        else:
            return int(parts[0])

    
    @staticmethod
    def format_time(seconds):
        """Format seconds into HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    
    @staticmethod
    def current_timestamp():
        """Get current timestamp in YYYY-MM-DD HH:MM:SS format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    