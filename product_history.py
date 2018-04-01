import csv
from os.path import join
from datetime import datetime
from finance_objects import PriceTimeBlock

__history_dir = './history'


def __parse_mt4_block(cross, csv_row):
    ptb = PriceTimeBlock()
    ptb.cross = cross
    ptb.date_time = datetime.strptime(csv_row[0] + " " + csv_row[1], "%Y.%m.%d %H:%M")
    ptb.price_open = csv_row[2]
    ptb.price_high = csv_row[3]
    ptb.price_low = csv_row[4]
    ptb.price_close = csv_row[5]
    return ptb


def __load_from_file(cross: str, interval: int):
    blocks = []

    with open(join(__history_dir, cross + str(interval) + '.csv'), 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for r in reader:
            blocks.append(__parse_mt4_block(cross, r))

    return blocks


def load_history(cross: str, interval: int):
    blocks = __load_from_file(cross, interval)
    return blocks
