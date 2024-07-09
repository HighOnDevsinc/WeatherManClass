''' Class Based Weather Man App '''

import os
import sys


''' class for storing the data associated with weather '''


class WeatherData:
    def __init__(self, pkt, max_temp_c, mean_temp_c, min_temp_c, dew_point_c,
                 mean_dew_point_c, min_dewpoint_c, max_humidity, mean_humidity,
                 min_humidity, max_sea_level_pressure_hpa,
                 mean_sea_level_pressure_hpa,
                 min_sea_level_pressure_hpa, max_visibility_km,
                 mean_visibility_km,
                 min_visibilitykm, max_wind_speed_kmh, mean_wind_speed_kmh,
                 max_gust_speed_kmh, precipitationmm, cloud_cover, events,
                 wind_dir_degrees):

        self.PKT = pkt
        self.MaxTemperatureC = max_temp_c
        self.MeanTemperatureC = mean_temp_c
        self.MinTemperatureC = min_temp_c
        self.DewPointC = dew_point_c
        self.MeanDewPointC = mean_dew_point_c
        self.MinDewpointC = min_dewpoint_c
        self.MaxHumidity = max_humidity
        self.MeanHumidity = mean_humidity
        self.MinHumidity = min_humidity
        self.MaxSeaLevelPressurehPa = max_sea_level_pressure_hpa
        self.MeanSeaLevelPressurehPa = mean_sea_level_pressure_hpa
        self.MinSeaLevelPressurehPa = min_sea_level_pressure_hpa
        self.MaxVisibilityKm = max_visibility_km
        self.MeanVisibilityKm = mean_visibility_km
        self.MinVisibilitykM = min_visibilitykm
        self.MaxWindSpeedKmh = max_wind_speed_kmh
        self.MeanWindSpeedKmh = mean_wind_speed_kmh
        self.MaxGustSpeedKmh = max_gust_speed_kmh
        self.Precipitationmm = precipitationmm
        self.CloudCover = cloud_cover
        self.Events = events
        self.WindDirDegrees = wind_dir_degrees


''' class for processing on the data of weather '''


class WeatherProcessor:

    def __init__(self, arguments):
        self.arguments = arguments
        self.data = []

    ''' a utility function for mapping month names against the month number '''
    @classmethod
    def mapping_months(cls, month_number):

        month_name = \
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec"
            ]

        return month_name[month_number - 1]

    ''' a utility function that resolves the incoming date into required
    format '''
    @classmethod
    def resolve_date(cls, date):
        date = date.split("-")
        date[1] = cls.mapping_months(int(date[1]))
        date.pop(0)
        s = " "
        return s.join(date)

    ''' a utility function to parse the command line arguments into usable
    form '''
    @classmethod
    def command_line_parsing(cls):

        arguments = []
        arg = sys.argv[1:]

        for x in arg:
            arguments.append(x)

        if "/" in arguments[1]:
            arguments[1] = arguments[1].split("/")
            arguments[1][1] = cls.mapping_months(int(arguments[1][1]))
            s = "_"
            arguments[1] = s.join(arguments[1])

        return arguments

    ''' function that takes command line arguments and processes the files and
    folders for extracting data '''
    def process_folder(self):
        files = os.listdir(self.arguments[2])

        for file in files:
            if self.arguments[1] in file:
                with open(self.arguments[2] + "/" + file) as file_object:
                    for line in file_object:
                        temp_tuple = line.strip().split(",")
                        if not temp_tuple or "<" in temp_tuple[0]:
                            break
                        if temp_tuple[0].isalpha() or temp_tuple == [""]:
                            continue
                        weather_data_obj = WeatherData(*temp_tuple)
                        self.data.append(weather_data_obj)

    ''' task 01 to extract values of highest temperature and day, lowest
    temperature and day and highest humidity and day in an year '''
    def yearly_value_temperatures_and_humidity(self):
        max_temp = float("-inf")
        min_temp = float("inf")
        max_humid = float("-inf")

        for extracted_tuple in self.data:

            # finding maximum temperature
            if extracted_tuple.MaxTemperatureC != "" and max_temp < \
                    int(extracted_tuple.MaxTemperatureC):
                max_temp = int(extracted_tuple.MaxTemperatureC)
                max_temp_day = self.resolve_date(extracted_tuple.PKT)

            # finding minimum temperature
            if extracted_tuple.MinTemperatureC != "" and min_temp > \
                    int(extracted_tuple.MinTemperatureC):
                min_temp = int(extracted_tuple.MinTemperatureC)
                min_temp_day = self.resolve_date(extracted_tuple.PKT)

            # finding maximum humidity
            if extracted_tuple.MaxHumidity != "" and max_humid < \
                    int(extracted_tuple.MaxHumidity):
                max_humid = int(extracted_tuple.MaxHumidity)
                max_humid_day = self.resolve_date(extracted_tuple.PKT)

        result = \
            [
                max_temp, max_temp_day,
                min_temp, min_temp_day,
                max_humid, max_humid_day
            ]

        return result

    ''' task 02 to extract values of highest average temperature, lowest
    average temperature and average humidity in a month '''
    def monthly_average_temperature_and_humidity(self):

        high_avg_temp = 0
        high_avg_temp_count = 0
        low_avg_temp = 0
        low_avg_temp_count = 0
        mean_avg_humid = 0
        mean_avg_humid_count = 0

        for extracted_tuple in self.data:

            # finding highest average temperature
            if extracted_tuple.MaxTemperatureC != "":
                high_avg_temp += int(extracted_tuple.MaxTemperatureC)
                high_avg_temp_count += 1

            # finding lowest average temperature
            if extracted_tuple.MinTemperatureC != "":
                low_avg_temp += int(extracted_tuple.MinTemperatureC)
                low_avg_temp_count += 1

            # finding mean average humidity
            if extracted_tuple.MeanHumidity != "":
                mean_avg_humid += int(extracted_tuple.MeanHumidity)
                mean_avg_humid_count += 1

        result = \
            [
                int(high_avg_temp / high_avg_temp_count),
                int(low_avg_temp / low_avg_temp_count),
                int(mean_avg_humid / mean_avg_humid_count)
            ]

        return result

    ''' task 03 to visualize a chart for highest temperature and lowest
    temperature of each day in a month '''
    def monthly_chart_temperature_and_humidity(self):

        chart = dict()
        chart = {"max_temp": [], "min_temp": []}

        for extracted_tuple in self.data:

            # finding highest average temperature
            if extracted_tuple.MaxTemperatureC != "":
                chart["max_temp"].append(extracted_tuple.MaxTemperatureC)

            # finding lowest average temperature
            if extracted_tuple.MinTemperatureC != "":
                chart["min_temp"].append(extracted_tuple.MinTemperatureC)

        return chart


''' main function of the program where the execution takes place '''


def main():
    arguments = WeatherProcessor.command_line_parsing()
    processor = WeatherProcessor(arguments)
    processor.process_folder()

    if processor.data != []:
        if arguments[0] == "-e":
            result = processor.yearly_value_temperatures_and_humidity()
            print("Highest:", result[0], "C on", result[1])
            print("Lowest:", result[2], "C on", result[3])
            print("Humid:", result[4], r"% on", result[5])

        elif arguments[0] == "-a":
            result = processor.monthly_average_temperature_and_humidity()
            print("Highest Average:", result[0], "C")
            print("Lowest Average:", result[1], "C")
            print("Average Humidity:", result[2], "%")

        elif arguments[0] == "-c":
            result = processor.monthly_chart_temperature_and_humidity()
            print(arguments[2])
            for x in range(len(result["max_temp"])):
                print(
                    x + 1,
                    " ",
                    "\033[1;32;40m*" * int(result["max_temp"][x]),
                    "\033[1;37;40m",
                    result["max_temp"][x],
                    "C"
                    )
                print(
                    x + 1,
                    " ",
                    "\033[1;34;40m*" * int(result["min_temp"][x]),
                    "\033[1;37;40m",
                    result["min_temp"][x],
                    "C"
                    )

        elif arguments[0] == "-b":
            result = processor.monthly_chart_temperature_and_humidity()
            print(arguments[2])
            for x in range(len(result["max_temp"])):
                print(
                    x + 1,
                    " ",
                    "\033[1;32;40m*" * int(result["max_temp"][x]),
                    "\033[1;34;40m*" * int(result["min_temp"][x]),
                    "\033[1;37;40m",
                    result["max_temp"][x],
                    "C -",
                    result["min_temp"][x],
                    "C"
                    )
    else:
        print("Empty data file provided")


''' caller with __name__ '''


if __name__ == "__main__":
    main()
