import os.path, sys

sys.path.append(os.path.dirname(__file__))
import datetime
from multiprocessing.dummy import active_children
import random
import os.path
import sys
# from random import randrange
# from datetime import timedelta, time
# from report_iterator import ReportIterator
from example_data import Example4Data
from server.input_factory import InputHandler
from common import data_structures


def read_file(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    file = open(file_path, "r")
    file_lines = []
    for line in file:
        file_lines.append(line.replace("\n", ""))
    return file_lines


def example1_hello_world():
    sheet_data = {
        'A1': 'Item',
        'B1': 'Cost',
        #
        'A2': 'Rent',
        'A3': 'Gas',
        'A4': 'Food',
        'A5': 'Gym',
        'A6': 'Total',
        #
        'B2': '10.10',
        'B3': '100.1',
        'B4': '300.5',
        'B5': '50.0',
        'B6': '=SUM(B1:B4)'
    }

    sheet = {
        'sheets': [
            {"Test Sheet": sheet_data}
        ]
    }
    return sheet


def example2_formats_simple():
    sheet_data = {
        'A1': {'value': 'Item', 'format': 'bold'},
        'B1': {'value': 'Cost', 'format': 'bold'},
        #
        '1,0': 'Rent',
        '2,0': 'Gas',
        '3,0': 'Food',
        '4,0': 'Gym',
        '5,0': 'Total',
        #
        '1,1': {'value': '50.50', 'format': 'number_bold_red'},
        '2,1': {'value': '15.88', 'format': 'number_bold_red'},
        '3,1': {'value': '33.90', 'format': 'number_bold_red'},
        '4,1': {'value': '80.55', 'format': 'number_bold_red'},
        '5,1': {'value': '=SUM(B2:B5)', 'format': 'number_bold_red'}
    }

    sheet = {
        'sheets': [
            {"Test Sheet": sheet_data},
        ],
        "formats": {
            'bold': {'bold': True},
            'bold_red': {'bold': True, 'font_color': 'red'},
            #
            'number': {'num_format': '$#,##.##'},
            'number_bold_red': {'bold': True, 'font_color': 'red', 'num_format': '$#,##.##'},
            'number_bold_blue': {'bold': True, 'font_color': 'red', 'bg_color': '#99CCFF', 'num_format': '$#,##.##'},

        }
    }
    return sheet


def example3_formats_more():
    sheet_data = {
        'A1': {'value': 'Item', 'format': 'bold'},
        'B1': {'value': 'Cost', 'format': 'bold'},
        'C1': {'value': 'Date', 'format': 'bold'},
        #
        '1,0': 'Rent',
        '2,0': 'Gas',
        '3,0': 'Food',
        '4,0': 'Gym',
        '5,0': 'Total',
        #
        '1,1': {'value': '500.50', 'format': 'number_bold_red'},
        '2,1': {'value': '150.88', 'format': 'number_bold_red'},
        '3,1': {'value': '330.90', 'format': 'number_bold_red'},
        '4,1': {'value': '80.55', 'format': 'number_bold_red'},
        '5,1': {'value': '=SUM(B2:B5)', 'format': 'sum_format'},
        #
        '1,2': {'date': '2013-01-01', 'format': 'date_format'},
        '2,2': {'date': '2013-02-01', 'format': 'date_format'},
        '3,2': {'date': '2013-03-01', 'format': 'date_format2'},
        '4,2': {'date': '2013-04-01', 'format': 'date_format2'},
        #


        "conditional_formats": {
            'B2:B5': {
                'type': 'cell', 'criteria': '>=', 'value': 300, 'format': 'number_bold_blue'
            }
        },
        #
        "column_size": {
            'A:B': 15,
            'C:C': 25
        }
    }

    sheet = {
        'sheets': [
            {"Test Sheet": sheet_data},
        ],
        "formats": {
            'bold': {'bold': True},
            'bold_red': {'bold': True, 'font_color': 'red'},
            #
            'number': {'num_format': '$#,##.##'},
            'number_bold_red': {'bold': True, 'font_color': 'red', 'num_format': '$#,##.##'},
            'number_bold_blue': {'bold': True, 'font_color': 'red', 'bg_color': '#99CCFF', 'num_format': '$#,##.##'},
            #
            'sum_format': {'bold': True, 'bg_color': '#E9AA94'},
            'date_format': {'num_format': 'yyyy d mmmm'},
            'date_format2': {'num_format': 'yy dd mmm'}
        }
    }
    return sheet

class Example4:

    def __init__(self):
        self.locations = read_file("locations")
        self.example4Data = Example4Data(self.locations)
        self.data = self.example4Data.create_data()
        self.sheets = []
        self.json_data = {}
        self.init_lambda()

    def init_lambda(self):
            self.to_string = lambda row, col: str(row) + "," + str(col)
            self.header_lambda = lambda row, col, to_string: (
                #returns ['0,0', '0,1', '1,0', '1,1'],['24,0', '24,1', '25,0', '25,1'] etc
                [to_string(r, c) for r, c in
                [(row, col), (row, col + 1), (row + 1, col), (row + 1, col + 1), (row + 2, col + 1)]]
            )

    def add_headers(self,sheet,row,col,arrival,departure):
        header_data = self.header_lambda(row, col,self.to_string)
        sheet[header_data[0]] = "Arrival"
        sheet[header_data[1]] = arrival
        sheet[header_data[2]] = "Departure"
        sheet[header_data[3]] = departure
        row = int(header_data[4].split(",")[0]) #(int(x) for x in header_data[4].split(","))
        return row

    def example4_realistic(self):
        row, col = 0, 0
        sheet = {}
        for k, v in self.data.items():
            departure, arrival, dates, companies = v["Departure"], v["Arrival"], v["dates"], v["companies"]
            row = self.add_headers(sheet,row,col,arrival,departure)

            for count, company_name in enumerate(companies.keys()):
                sheet[self.to_string(row, count + 1)] = company_name

            def add_prices(row, date_to_match, description):
                col = 1;
                for company, dates in companies.items():
                    for date_in_company in dates[description]:
                        date_found = data_structures.get_dict(date_in_company, date_to_match)
                        if date_found:
                            sheet[ self.to_string(row, col)] = date_found
                    col += 1

            def add_dates(row):
                for description_count, description in enumerate(dates.keys()):
                    description_row = description_count + row
                    sheet[ self.to_string(description_row, 0)] = description
                    date_values = dates[description]
                    for date_count, date in enumerate(date_values):
                        date_row = description_row + date_count + 1
                        sheet[ self.to_string(date_row, 0)] = date.strftime('%m/%d/%Y')
                        add_prices(date_row, date, description)
                    row += len(date_values)
                return row + len(dates.keys()) + 1

            row = add_dates(row + 1)

        self.sheets.append({"sheet": sheet})
        self.json_data["sheets"] = self.sheets
        print(self.json_data)
        return self.json_data



#example4.example4_realistic()

def example4_realistic():
    return Example4().example4_realistic()

functions = {"1": example1_hello_world(),
             "2": example2_formats_simple(),
             "3": example3_formats_more(),
             "4": example4_realistic()
}