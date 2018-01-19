#!/usr/bin/env python

import openpyxl
import sys
import json

def extract_area_from_excel_doc(fn, topleftcell, bottomrightcell):
    wb = openpyxl.load_workbook(fn)
    ws = wb.active
    return [[ cell.value for cell in row ] for row in ws[topleftcell:bottomrightcell]]

def obj_from_matrix(mx):
    obj = {}
    for i in range(1, len(mx)):
        entry = obj[mx[i][0]] = {}
        for j in range(1, len(mx[0])):
            entry[mx[0][j]] = mx[i][j]
    return obj


def show_usage():
    print("Usage: ./xlstabletojson document.xlsx topleftcell:bottomrightcell")
    print("Example: ./xlstabletojson mydata.xlsx B2:H24")

def main(args):
    if len(args) != 3:
        show_usage()
    else:
        parts = args[2].split(':')
        with open(args[1].replace('.xlsx', '.json'), 'w') as fp:
            json.dump(obj_from_matrix(extract_area_from_excel_doc(args[1], parts[0], parts[1])), fp, indent=4, sort_keys=True)

if __name__ == '__main__':
    main(sys.argv)