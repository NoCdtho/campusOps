# Buidling metadata the operating_hours are considered randomly but are fixed  

HOSTELS = [
    {
        "hostel_id": "1",
        "name": "SNM",
        "operating_hours": "08:00-18:00",
        "base_power_kw": 120.0,  # Expected baseline power consumption during active hours
        "off_hours_base_kw": 25.0,
    },
    {
        "hostel_id": "2",
        "name": "JD",
        "operating_hours": "07:00-19:00",
        "base_power_kw": 200.0,
        "off_hours_base_kw": 40.0,
    },
    {
        "hostel_id": "3",
        "name": "SJ",
        "operating_hours": "00:00-23:59",  # 24/7 Facility
        "base_power_kw": 450.0,
        "off_hours_base_kw": 430.0,
    },
    {
        "hostel_id": "4",
        "name": "Gambari",
        "operating_hours": "06:00-22:00",
        "base_power_kw": 80.0,
        "off_hours_base_kw": 15.0,
    },
]