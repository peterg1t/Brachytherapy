###########################################################################################
#
#   Script name: Oncentra_DicomTag
#
#   Description: Tool for viewing Dicom tags
#
#   Example usage: python Oncentra_DicomTag "/file/"
#
#   Author: Pedro Martinez
#   pedro.enrique.83@gmail.com
#   5877000722
#   Date:2019-05-10
#
###########################################################################################



import os
import pydicom
import argparse




def process_dicom(filename):
    dataset = pydicom.dcmread(filename)
    print(dataset)
    exit(0)



parser = argparse.ArgumentParser() #pylint: disable = invalid-name
parser.add_argument('-f', '--filename', help='path to file')
args = parser.parse_args() #pylint: disable = invalid-name

if args.filename:
    filename = args.filename  #pylint: disable = invalid-name
    process_dicom(filename)

