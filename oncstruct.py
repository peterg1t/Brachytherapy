"""
Script name: oncstruct

Description: Tool for processing of Oncentra structure files

Author: Pedro Martinez
pedro.enrique.83@gmail.com
5877000722
Date:2019-05-10

"""

import os
from mayavi import mlab

import numpy as np
import csv
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import pydicom


# using mayavi
def process_file(filename):
    dirname=os.path.dirname(filename)
    base=os.path.basename(filename)
    file =os.path.splitext(base)
    # using matplotlib
    # def process_file(filename, fig, ax):
    dataset = pydicom.dcmread(filename)
    roi_num = []
    xs_tot = []
    ys_tot = []
    zs_tot = []
    element = []
    desc_item = []
    color = []
    layer = []

    for item in dataset[0x3006, 0x0020]:
        desc_item.append(
            (
                int(item[0x3006, 0x0022].value),
                #item[0x3006, 0x0088].value,
                item[0x3006, 0x0026].value,
            )
        )

    desc_item = np.asarray(desc_item)

    k = 0
    for elem in dataset[0x3006, 0x0039]:  # CTV, lesion, etc
        xs_el = []
        ys_el = []
        zs_el = []
        roi_color = np.asarray(elem[0x3006, 0x002A].value)
        # print(roi_color/255,np.shape(roi_color))
        # exit(0)
        hex_color = colors.rgb2hex(np.asarray(roi_color) / 255)
        roi_num.append(elem[0x3006, 0x0084].value)
        kk = 0
        try:
            for contour in elem[0x3006, 0x0040]:
                xs_sl = []
                ys_sl = []
                zs_sl = []
                for i in range(0, contour[0x3006, 0x0050].VM, 3):
                    xs_tot.append(contour[0x3006, 0x0050][i])
                    ys_tot.append(contour[0x3006, 0x0050][i + 1])
                    zs_tot.append(contour[0x3006, 0x0050][i + 2])
                    xs_el.append(contour[0x3006, 0x0050][i])
                    ys_el.append(contour[0x3006, 0x0050][i + 1])
                    zs_el.append(contour[0x3006, 0x0050][i + 2])
                    xs_sl.append(contour[0x3006, 0x0050][i])
                    ys_sl.append(contour[0x3006, 0x0050][i + 1])
                    zs_sl.append(contour[0x3006, 0x0050][i + 2])
                    color.append(roi_color)
                    element.append(desc_item[k, :])
                    layer.append(kk)
                    # print('kk=',kk)
                kk = kk + 1
                print('slice=',kk,'x_ave=', np.average(xs_sl))
                print('slice=',kk,'y_ave=', np.average(ys_sl))
                print('slice=',kk,'z_ave=', np.average(zs_sl))

            # #using matplotlib3d
            # verts = [list(zip(xs_el, ys_el, zs_el))]
            # poly = Poly3DCollection(verts, alpha=0.5)
            # poly.set_color(hex_color)
            # poly.set_edgecolor('k')
            # ax.add_collection3d(poly)

            # using mayavi (temporary until I figure how to make closed surfaces)
            col = (roi_color[0] / 255, roi_color[1] / 255, roi_color[2] / 255)
            mlab.plot3d(xs_el, ys_el, zs_el, tube_radius=0.1, color=col)


            # here we print the center of mass of the structre, defined as the average of the x, y and z components,
            print('x_ave=',np.average(xs_el))
            print('y_ave=',np.average(ys_el))
            print('z_ave=',np.average(zs_el))


            # Do you you want to save csv files of every structure in the dicom file
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
                elem = np.transpose(np.vstack((xs_el,ys_el,zs_el)))
                with open(dirname+"/"+file[0]+"_"+str(desc_item[k,1])+".csv","w+") as my_csv:            # writing the file as my_csv
                #with open(dirname+"/"+file[0]+"_struct"+str(k)+".csv","w+") as my_csv:            # writing the file as my_csv
                    csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
                    csvWriter.writerow(['x','y','z'])
                    csvWriter.writerows(elem)


        except:
            print("no contour data")

        k = k + 1

    # #using matplotlib3d (preparing figure)
    # ax.set_xlim3d(np.min(xs_tot), np.max(xs_tot))
    # ax.set_ylim3d(np.min(ys_tot), np.max(ys_tot))
    # ax.set_zlim3d(np.min(zs_tot), np.max(zs_tot))
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    # plt.show()

    elem_data = np.transpose(
        np.vstack(
            (
                np.transpose(element),
                np.transpose(np.asarray(color)),
                layer,
                xs_tot,
                ys_tot,
                zs_tot,
            )
        )
    )

    return (
        elem_data
    )  # returning a matrix with all the data containing (element number, element description(CTV1,Urethra,etc.), element type (PTV,etc.),color, contour/layer and point location (x,y,z))
