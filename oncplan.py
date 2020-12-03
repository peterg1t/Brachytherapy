"""
Script name: oncplan

Description: Tool for processing of Oncentra plan files

Author: Pedro Martinez
pedro.enrique.83@gmail.com
5877000722
Date:2019-05-10

"""


import os
import sys

from mayavi import mlab

import numpy as np
import csv
import pydicom

sys.path.append("C:\Program Files\GDCM 2.8\lib")


# def process_file(filename,ax):
def process_file(filename):
    dirname=os.path.dirname(filename)
    base=os.path.basename(filename)
    file =os.path.splitext(base)
    dataset = pydicom.dcmread(filename)
    source_dataset = []
    xs = []
    ys = []
    zs = []
    ts = []

    for elem in dataset[0x300A, 0x0230][0][0x300A, 0x0280]:
        for pos in elem[0x300A, 0x02D0]:
            x, y, z = pos[0x300A, 0x02D4].value
            source_dataset.append(
                [
                    elem[0x300A, 0x0282].value,
                    elem[0x300A, 0x0284].value,
                    elem[0x300A, 0x0286].value,
                    pos[0x300A, 0x0112].value,
                    x,
                    y,
                    z,
                    pos[0x300A, 0x02D6].value,
                ]
            )

    source_dataset = np.asarray(source_dataset)
    print(source_dataset.shape)
    for i in range(1, source_dataset.shape[0], 2):
        x = source_dataset[i, 4]
        y = source_dataset[i, 5]
        z = source_dataset[i, 6]
        tw = source_dataset[i, 7] - source_dataset[i - 1, 7]
        xs.append(x)
        ys.append(y)
        zs.append(z)
        ts.append(tw / 100 * source_dataset[i, 2])
        # print('tw=',tw,source_dataset[i,7],source_dataset[i-1,7])

# Do you you want to save csv files of plan in the dicom file
    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Do you you want to save csv files of structure "+str(desc_item[k, :])+" in the dicom file? [yes(y)/no(n)]> ")
        try:
            ##        if line == 'done':
            ##            break
            ioption = str(line.lower())
            if ioption.startswith(("y", "yeah", "yes", "n", "no", "nope")):
                break
        except:  # pylint: disable = bare-except
            print("Please enter a valid option:")
    if ioption.startswith(("y", "yeah", "yes")):
        elem = np.transpose(np.vstack((xs,ys,zs,ts)))
        with open(dirname+"/"+file[0]+"_"+".csv","w+") as my_csv:            # writing the file as my_csv
        #with open(dirname+"/"+file[0]+"_struct"+str(k)+".csv","w+") as my_csv:            # writing the file as my_csv
            csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
            csvWriter.writerow(['x','y','z','t'])
            csvWriter.writerows(elem)

    # for matplotlib3d
    # ax.scatter(xs, ys, zs, s=ts)

    # for mayavi
    return xs, ys, zs, ts  # returning the positions of the sources and the dwell time
