from GARMIN_data import connecting as gcon
import datetime


start_date = datetime.date(2023, 12, 7)
end_date = datetime.date.today()

# Link with Garmin-Connect account
email = input("Email: ")
password = input("Password: ")

api = gcon.init_garmin_api(email, password)
gcon.save_data(api, start_date, end_date)