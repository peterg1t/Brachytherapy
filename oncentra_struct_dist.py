import os
import sys
import pandas as pd
import numpy as np
import pydicom
import argparse
import math


os.environ["ETS_TOOLKIT"] = "wx"
np.set_printoptions(threshold=sys.maxsize)





def process_struct(filename, dirname):
    print("Starting struct calculation")
    dataset = pydicom.dcmread(filename)

    k = 0
    for elem in dataset[0x3006, 0x0020]:
        print(elem[0x3006, 0x0028].value, k)
        k = k + 1


    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Select the first structure > ")
        try:
            num1 = int(line.lower())  # temporarily since allows any range of numbers
            break
        except ValueError:  # pylint: disable = bare-except
            print("Please enter a valid option:")


    while True:  # example of infinite loops using try and except to catch only numbers
        line = input("Select the second structure > ")
        try:
            num2 = int(line.lower())  # temporarily since allows any range of numbers
            break
        except ValueError:  # pylint: disable = bare-except
            print("Please enter a valid option:")


    structset=[num1,num2]
    struct__names_list = [dataset[0x3006, 0x0020][num1][0x3006, 0x0028].value,dataset[0x3006, 0x0020][num2][0x3006, 0x0028].value]



    
    dz = abs(
        dataset[0x3006, 0x0039][num1][0x3006, 0x0040][2][0x3006, 0x0050][2]
        - dataset[0x3006, 0x0039][num1][0x3006, 0x0040][1][0x3006, 0x0050][2]
    )
    print("dz=", dz)


    k=0
    for struct in structset:
        elem = dataset[0x3006, 0x0039][struct]
        xs_elem = []
        ys_elem = []
        zs_elem = []
        try:
            for contour in elem[0x3006, 0x0040]:  
                for i in range(0, contour[0x3006, 0x0050].VM, 3):
                    xs_elem.append(contour[0x3006, 0x0050][i])
                    ys_elem.append(contour[0x3006, 0x0050][i+1])
                    zs_elem.append(contour[0x3006, 0x0050][i+2])

            x_elem = np.array(xs_elem).astype(np.float)  # this is the collection of points for every element
            y_elem = np.array(ys_elem).astype(np.float)
            z_elem = np.array(zs_elem).astype(np.float)
            if k == 0: #if structure 0
                elem_0 = np.stack((x_elem, y_elem, z_elem), axis=1)
            if k == 1: #if structure 0
                elem_1 = np.stack((x_elem, y_elem, z_elem), axis=1)


        except:  # pylint: disable = bare-except
            print("no contour data")    
    
        k=k+1



    min_dist=999999999999
    for i in range(0,np.shape(elem_0)[0]):
        for j in range(0,np.shape(elem_1)[0]):
            dist = math.sqrt ( (elem_0[i,0]-elem_1[j,0])*(elem_0[i,0]-elem_1[j,0]) +  (elem_0[i,1]-elem_1[j,1])*(elem_0[i,1]-elem_1[j,1]) + (elem_0[i,2]-elem_1[j,2])*(elem_0[i,2]-elem_1[j,2])  )
            if dist < min_dist:
                min_dist=dist

    print('Minimum distance between contours=',min_dist,'mm')
    exit(0)








if __name__ == "__main__":
    parser = argparse.ArgumentParser()


    parser.add_argument("structure", type=str, help="Input the structure file")


    args = parser.parse_args()



    if args.structure:
        sname = args.structure
        dname = os.path.dirname(sname)
        process_struct(sname,dname)        

