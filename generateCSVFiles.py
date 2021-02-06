#!/usr/bin/env python3

import csv
import random
import logging

def write_file(filename, start, end):

    with open(filename, mode='w') as ref_file:
        writer = csv.writer(ref_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(start, end):
            for j in range(1, 1001):
                value = random.random()
                writer.writerow([i, value])
                # print("row: ", i, j, value)

def main():
    write_file("ref1.csv", 1, 333333)
    write_file("ref2.csv", 333333, 666666)
    write_file("ref3.csv", 666666, 1000001)

if __name__ == "__main__":
    main()
