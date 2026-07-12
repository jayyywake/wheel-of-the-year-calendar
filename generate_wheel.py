import ephem
import math
import datetime
from ics import Calendar, Event

def get_solar_lon(date):
    sun = ephem.Sun()
    sun.compute(date)
    ecl = ephem.Ecliptic(sun)
    return math.degrees(ecl.lon)

def generate_wheel_calendar():
    cal = Calendar()
    today = datetime.datetime.utcnow().date()
    
    # The 8 solar stations mapped to their exact ecliptic degrees
    stations = {
        0: "Spring Equinox",
        45: "Beltane (15° Taurus)",
        90: "Summer Solstice",
        135: "Lughnasadh (15° Leo)",
        180: "Autumn Equinox",
        225: "Samhain (15° Scorpio)",
        270: "Winter Solstice",
        315: "Imbolc (15° Aquarius)"
    }
    
    prev_lon = get_solar_lon(today)
    
    for i in range(1, 365):
        current_date = today + datetime.timedelta(days=i)
        lon = get_solar_lon(current_date)
        
        for target_deg, name in stations.items():
            # Handle the 360 to 0 degree wrap-around for the Spring Equinox
            if target_deg == 0:
                if prev_lon > 350 and lon < 10:
                    e = Event(name=name, begin=current_date)
                    e.make_all_day()
                    cal.events.add(e)
            # Handle all other degrees
            else:
                if prev_lon < target_deg and lon >= target_deg:
                    e = Event(name=name, begin=current_date)
                    e.make_all_day()
                    cal.events.add(e)
                    
        prev_lon = lon
        
    with open("wheel_of_the_year.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    generate_wheel_calendar()
