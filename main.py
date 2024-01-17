from GARMIN_data import connecting as gcon
from GARMIN_data import garmin_function as gf
import datetime


start_date = datetime.date(2023, 12, 7)
end_date = datetime.date.today()

# Link with Garmin-Connect account
email = input("Email: ")
password = input("Password: ")

api = gcon.init_garmin_api(email, password)
gf.save_data(api, start_date, end_date)

gcon.logout_garmin_api(api)