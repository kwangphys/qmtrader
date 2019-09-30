if __name__ == '__main__':
    from yahoo.tasks import *
    import datetime

    start_date = datetime.datetime(2018, 5, 1)
    end_date = datetime.datetime.today()
    folder = "X:\\Trading\\USFundamentals"
    d = start_date
    while d <= end_date:
        print(d)
        daily_write_to_db(d, folder)
        d = d + datetime.timedelta(days=1)
    print('Done')
