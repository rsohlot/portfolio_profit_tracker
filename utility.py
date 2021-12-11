from datetime import date, datetime


def get_current_date(format='%d-%m-%Y'):
    today = date.today()
    return today.strftime(format)

def get_data_path():
    path = 'data/reports/'
    return path

def format_date(date, format='%d-%m-%Y'):
    if isinstance(date, str):
        date = datetime.strptime(date,'%Y-%m-%d')
    return date.strftime(format)