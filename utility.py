from datetime import date


def get_current_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")

def get_data_path():
    path = 'data/reports/'
    return path