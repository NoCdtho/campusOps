import time
import json
import datetime 
from typing import Dict, List
import random 
from Hostel import HOSTELS 

class EnergySimulator:

    def __init__(self, interval_seconds: int = 15): # here interval hour is used to convert the power into energy
        self.hostels = HOSTELS
        self.interval_seconds = interval_seconds
        self.reading_counter = 1000

    # Check if the op time is still active for any hostel
    def _is_operating_hour(self, current_time: datetime.datetime, op_hours: str) -> bool:
        start_str, end_str = op_hours.split("-")
        start_time = datetime.datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_str, "%H:%M").time()
        current_time2 = current_time.time()
        return start_time <= current_time2 <= end_time

    # calculate the observed vs expected values and in 
    def _generate_data(self, hostel: Dict, current_time: datetime.datetime) -> Dict:

        is_active = self._is_operating_hour(current_time, hostel["operating_hours"])
        expected_power_kw: int = 0
        if is_active:
            expected_power_kw = hostel["base_power_kw"]
        else:
            expected_power_kw = hostel["off_hours_base_kw"]

        observed_power_kw = expected_power_kw
        severity = "NORMAL"

        anomaly_roll = random.random()
        
        if anomaly_roll < 0.05:
            # Issue Type 1: High Surge / HVAC Failure Spike
            observed_power_kw = round(expected_power_kw * random.uniform(1.6, 2.5), 2)
            severity = "HIGH"
        elif anomaly_roll < 0.10 and not is_active:
            # Issue Type 2: Off-Hours Leakage (Equipment or lighting left running)
            observed_power_kw = round(hostel["base_power_kw"] * random.uniform(0.8, 1.1), 2)
            severity = "MEDIUM"
        elif anomaly_roll < 0.15:
            # Issue Type 3: Minor inefficiency / abnormal baseline shift
            observed_power_kw = round(expected_power_kw * random.uniform(1.25, 1.45), 2)
            severity = "LOW"

        interval_hours = self.interval_seconds / 3600.0
        energy_kwh = round(observed_power_kw * interval_hours, 4)
        self.reading_counter += 1

        return {
            "reading_id": f"READ-{self.reading_counter}",
            "building_id": hostel["hostel_id"],
            "building_name": hostel["name"],
            "operating_hours": hostel["operating_hours"],
            "timestamp": current_time.isoformat(),
            "power_kw": observed_power_kw,
            "energy_kwh": energy_kwh,
            "observed_value": observed_power_kw,
            "expected_value": expected_power_kw,
            "severity": severity,
        }

    #Generates a batch of historical readings (useful for seeding databases).
    def generate_batch(self, count_per_hostel: int = 10) -> List[Dict]:
        data = []
        now = datetime.datetime.now(datetime.timezone.utc)
        for b in self.hostels:
            for i in range(count_per_hostel):
                ts = now - datetime.timedelta(seconds=(count_per_hostel- i) * self.interval_seconds)
                data.append(self._generate_data(b, ts))
        return data

    # Simulates real-time energy telemetry stream.
    def stream_live(self, callback_fn=None):

        print("Starting real-time energy simulator stream... Press Ctrl+C to stop.\n")
        try:
            while True:
                now = datetime.datetime.now(datetime.timezone.utc)
                for hostel in self.hostels:
                    reading = self._generate_data(hostel, now)
                    if callback_fn:
                        callback_fn(reading)
                    else:
                        print(json.dumps(reading, indent=2))
                time.sleep(self.interval_seconds)
        except KeyboardInterrupt:
            print("\nSimulator stopped.")


simulator = EnergySimulator(interval_seconds=5)
batch_readings = simulator.generate_batch(count_per_hostel=2)
print("Sample record:", json.dumps(batch_readings[0], indent=2))