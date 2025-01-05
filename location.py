import geocoder


class GetLocation:
    def __init__(self) -> None:
        self.location = None
        self.api_key = 'ca499784a0b3403e8d7eebfeb0b33ef9'

    def get_location(self) -> None:
        g = geocoder.ip('me', key=self.api_key)

        if g.ok:
            self.location = g.json
        else:
            print("Geocoding request failed.")
            return None

    def return_location(self) -> str:
        self.get_location()

        if self.location:
            return self.create_google_maps_link(self.location['lat'], self.location['lng'])

    def create_google_maps_link(self, latitude, longitude):
        base_url = "https://www.google.com/maps/search/?api=1&query="
        return base_url + str(latitude) + "," + str(longitude)
