from datetime import date

def today_date():
    today = date.today()
    today_date = today.strftime("%d-%m-%Y")
    # print(today_date)

    return today_date

print(today_date())