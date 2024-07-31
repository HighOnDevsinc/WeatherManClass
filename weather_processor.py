from weather_data import WeatherData
import sys
import os


# defined a dictionary for mapping months
month_dict = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}


class WeatherProcessor:

    ''' class for processing on the data of weather '''

    def __init__(self, arguments):
        self.arguments = arguments
        self.data = []

    @classmethod
    def resolve_date(cls, date):

        ''' a utility function that resolves the incoming date into required
    format '''

        date = date.split("-")
        date[1] = month_dict.get(int(date[1]))
        date.pop(0)
        s = " "
        return s.join(date)

    @classmethod
    def command_line_parsing(cls):

        ''' a utility function to parse the command line arguments into usable
    form '''

        folder_choices = ["Dubai_weather", "lahore_weather", "Murree_weather"]
        arguments = []
        arg = sys.argv[1:]

        for x in arg:
            arguments.append(x)

        temp = arguments[2].split("/")
        if temp[-1] not in folder_choices:
            return False

        if "/" in arguments[1]:
            arguments[1] = arguments[1].split("/")
            arguments[1][1] = month_dict.get(int(arguments[1][1]),
                                             "Invalid month number")
            s = "_"
            arguments[1] = s.join(arguments[1])

        return arguments

    def process_folder(self):

        ''' function that takes command line arguments and processes the files
    and folders for extracting data '''

        files = os.listdir(self.arguments[2])

        file_paths = [
            f"{self.arguments[2]}/{file}" for file in files
            if self.arguments[1] in file
            ]

        for file_path in file_paths:
            with open(file_path) as file_object:
                for line in file_object:
                    temp_tuple = line.strip().split(",")
                    if not temp_tuple or "<" in temp_tuple[0]:
                        break
                    if temp_tuple[0].isalpha() or temp_tuple == [""]:
                        continue
                    temp_tuple = [temp_tuple[x] for x in sorted(
                        [0, 1, 3, 7, 8])]
                    weather_data_obj = WeatherData(*temp_tuple)
                    self.data.append(weather_data_obj)

    def yearly_value_temperatures_and_humidity(self):

        ''' task 01 to extract values of highest temperature and day, lowest
    temperature and day and highest humidity and day in an year '''

        max_temp = float("-inf")
        min_temp = float("inf")
        max_humid = float("-inf")

        for extracted_tuple in self.data:

            # finding maximum temperature
            if extracted_tuple.max_temperature != "" and max_temp < \
                    float(extracted_tuple.max_temperature):
                max_temp = float(extracted_tuple.max_temperature)
                max_temp_day = self.resolve_date(extracted_tuple.time_zone)

            # finding minimum temperature
            if extracted_tuple.min_temperature != "" and min_temp > \
                    float(extracted_tuple.min_temperature):
                min_temp = float(extracted_tuple.min_temperature)
                min_temp_day = self.resolve_date(extracted_tuple.time_zone)

            # finding maximum humidity
            if extracted_tuple.max_humidity != "" and max_humid < \
                    float(extracted_tuple.max_humidity):
                max_humid = float(extracted_tuple.max_humidity)
                max_humid_day = self.resolve_date(extracted_tuple.time_zone)

        result = \
            [
                max_temp, max_temp_day,
                min_temp, min_temp_day,
                max_humid, max_humid_day,
            ]

        return result

    def monthly_average_temperature_and_humidity(self):

        ''' task 02 to extract values of highest average temperature, lowest
    average temperature and average humidity in a month '''

        high_avg_temp = 0
        high_avg_temp_count = 0
        low_avg_temp = 0
        low_avg_temp_count = 0
        mean_avg_humid = 0
        mean_avg_humid_count = 0

        for extracted_tuple in self.data:

            # finding highest average temperature
            if extracted_tuple.max_temperature != "":
                high_avg_temp += float(extracted_tuple.max_temperature)
                high_avg_temp_count += 1

            # finding lowest average temperature
            if extracted_tuple.min_temperature != "":
                low_avg_temp += float(extracted_tuple.min_temperature)
                low_avg_temp_count += 1

            # finding mean average humidity
            if extracted_tuple.mean_humidity != "":
                mean_avg_humid += float(extracted_tuple.mean_humidity)
                mean_avg_humid_count += 1

        result = \
            [
                float(high_avg_temp / high_avg_temp_count),
                float(low_avg_temp / low_avg_temp_count),
                float(mean_avg_humid / mean_avg_humid_count),
            ]

        return result

    def monthly_chart_temperature_and_humidity(self):

        ''' task 03 to visualize a chart for highest temperature and lowest
    temperature of each day in a month '''

        chart = dict()
        chart = {"max_temp": [], "min_temp": []}

        for extracted_tuple in self.data:

            # finding highest average temperature
            if extracted_tuple.max_temperature != "":
                chart["max_temp"].append(extracted_tuple.max_temperature)

            # finding lowest average temperature
            if extracted_tuple.min_temperature != "":
                chart["min_temp"].append(extracted_tuple.min_temperature)

        return chart
