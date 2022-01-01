from datetime import date, datetime
from dateutil import parser

striped_date_format ="%d-%m-%Y"

def get_current_date(format=striped_date_format):
    today = date.today()
    return today.strftime(format)

def get_data_path():
    path = 'data/reports/'
    return path

def format_date(date, format=striped_date_format):
    if isinstance(date, str):
        # date = parser.parse(date)
        date = datetime.strptime(date,'%Y-%m-%d')
    return date.strftime(format)

def merge_same_cols(cls,df):
    # refernce : https://stackoverflow.com/questions/69299416/combine-two-columns-with-same-column-name-using-pandas
    if len(df.columns[df.columns.duplicated()]) > 0:
        df = (df.set_axis(pd.MultiIndex.from_arrays([df.columns,
                                                        df.groupby(level=0, axis=1).cumcount()
                                                    ]), axis=1)
                .stack(level=1)
                .sort_index(level=1)
                .droplevel(1)
                .drop_duplicates(subset=df.columns[df.columns.duplicated()])
                )
    else:
        pass
    return df