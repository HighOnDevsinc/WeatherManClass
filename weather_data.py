class WeatherData:

    ''' class for storing the data associated with weather '''

    def __init__(
            self,
            pkt,
            max_temp_c,
            min_temp_c,
            max_humid,
            mean_humid,
            ):

        self.time_zone = pkt
        self.max_temperature = max_temp_c
        self.min_temperature = min_temp_c
        self.max_humidity = max_humid
        self.mean_humidity = mean_humid
