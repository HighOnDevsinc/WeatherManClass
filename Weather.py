# Class based weather man app

from weather_processor import WeatherProcessor


def main():

    ''' main function of the program where the execution takes place '''

    arguments = WeatherProcessor.command_line_parsing()

    if arguments:

        processor = WeatherProcessor(arguments)
        processor.process_folder()

        if processor.data != []:

            if arguments[0] == "-e":
                result = processor.yearly_value_temperatures_and_humidity()
                print(f"Highest: {result[0]:.0f} C on {result[1]}\n" +
                      f"Lowest: {result[2]:.0f} C on {result[3]}\n" +
                      f"Humid: {result[4]:.0f}% on {result[5]}")

            elif arguments[0] == "-a":
                result = processor.monthly_average_temperature_and_humidity()
                print(f"Highest Average: {result[0]:.2f} C\n" +
                      f"Lowest Average: {result[1]:.2f} C\n" +
                      f"Average Humidity: {result[2]:.2f} %")

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
                print("Enter valid arguments")
        else:
            print("Enter valid arguments")
    else:
        print("Enter valid arguments")


''' caller with __name__ '''


if __name__ == "__main__":
    main()
