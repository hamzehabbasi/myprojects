from Business.models import Taxi


def api(self, for_id=False):
    response = {
        "key": self.key,
        "car_type": self.car_type,
        "taxi_code": self.taxi_code,

        "taxi_license_plate": self.taxi_license_plate,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed
    }
    if not for_id:
        response["taxi_driver"] = self.taxi_driver.api()

    return response


def load_taxis_v1abcd12(_, d, device):
    taxi = Taxi.g(taxi_driver__exact=device.user)
    return [taxi.api()] if taxi else []
