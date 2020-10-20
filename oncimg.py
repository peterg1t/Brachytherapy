"""
Script name: oncdose

Description: Tool for processing of Oncentra dose files

Author: Pedro Martinez
pedro.enrique.83@gmail.com
5877000722
Date:2019-05-10

"""


from mayavi import mlab
import os
import numpy as np


import matplotlib.pyplot as plt

import pydicom


# def process_file(filename,ax,fig):
def process_file(filename):
    """This function process an image dicom file  """
    # print('Starting dose calculation')
    dataset = pydicom.dcmread(filename)
    # print(dataset)
    array_dicom = np.zeros(
        (dataset.Rows, dataset.Columns, 0), dtype=dataset.pixel_array.dtype
    )
    array_dicom = dataset.pixel_array

    dz = dataset.SliceThickness  # pylint: disable = invalid-name
    dy, dx = dataset.PixelSpacing  # pylint: disable = invalid-name
    origin = dataset[0x0020, 0x0032].value
    print("pixel spacing depth [mm]=", dz)
    print("pixel spacing row [mm]=", dy)
    print("pixel spacing col [mm]=", dx)
    print("origin=", origin)
    # exit(0)

    # for mayavi
    x, y, z = np.mgrid[
        origin[0] : origin[0] + ((array_dicom.shape[2]-0.5) * dx) : dx, #not clear why the 0.5 but it seems the only way to get the correct grid. I need to investigate this further
        origin[1] : origin[1] + ((array_dicom.shape[1]-0.5) * dy) : dy,
        origin[2] - (array_dicom.shape[0] * dz) : origin[2] : dz,
    ]  # pylint: disable = invalid-name
    volume = np.flip(
        np.swapaxes(array_dicom, axis1=0, axis2=2), axis=2
    )  # need to swap two axis and flip z since the axis must be increasing
    volume = np.swapaxes(volume, axis1=0, axis2=1) #axes x and y must also be flipped

    # print(x[0:np.shape(x)[0],0,0],np.shape(x)[0], np.shape(y), np.shape(z), np.shape(volume))
    # print(origin[0] , origin[0] + ((array_dicom.shape[2]-1) * dx) , dx)

    return x, y, z, dx, dy, dz, volume








# def process_file(filename,ax,fig):
def process_directory(dirname):
    """This function process a series image dicom file  """
    slice_unsrt = [] #this will hold the slice numbers for re-sorting
    origin=[]
    for subdir, dirs, files in os.walk(dirname):
        k = 0
        # for file in tqdm(sorted_nicely(files)):
        for file in files:
            if file.endswith('.dcm'):
                dataset = pydicom.dcmread(dirname + file, force=True)
                if k == 0:
                    ArrayDicom = np.zeros((dataset.Rows, dataset.Columns, 0), dtype=dataset.pixel_array.dtype)
                    ArrayDicom = np.dstack((ArrayDicom, dataset.pixel_array))
                    slice_unsrt.append(int(dataset[0x0020, 0x0013].value))
                    dz = dataset.SliceThickness  # pylint: disable = invalid-name
                    dy, dx = dataset.PixelSpacing  # pylint: disable = invalid-name
                    origin.append(dataset[0x0020, 0x0032].value)  # we need the corner of the entire dataset so this might not be correct
                else:
                    ArrayDicom = np.dstack((ArrayDicom, dataset.pixel_array))
                    slice_unsrt.append(int(dataset[0x0020, 0x0013].value))
                    origin.append(dataset[0x0020, 0x0032].value)  # we need the corner of the entire dataset so this might not be correct

            k = k + 1

            # we have loaded the image but the spacing is different in the x,y and z directions
            # spacing = map(float, ([scan[0].SliceThickness] + scan[0].PixelSpacing))
            # spacing = np.array(list(spacing))
            # print(np.shape(ArrayDicom))
    origin = np.asarray(origin)
    OArrayDicom = np.copy(ArrayDicom)
    oorigin = np.copy(origin)


    for count, sl in enumerate(slice_unsrt):
        # print(count, sl)
        OArrayDicom[:, :, sl - 1] = ArrayDicom[:, :, count]
        oorigin[sl-1,:] = origin[count,:]




    print("pixel spacing depth [mm]=", dz)
    print("pixel spacing row [mm]=", dy)
    print("pixel spacing col [mm]=", dx)
    print("origin=", oorigin[0,:])

    # for mayavi
    x, y, z = np.mgrid[
        oorigin[0,0] : oorigin[0,0] + ((OArrayDicom.shape[0]-0.5) * dx) : dx,
        oorigin[0,1] : oorigin[0,1] + ((OArrayDicom.shape[1]-0.5) * dy) : dy,
        oorigin[0,2] - (OArrayDicom.shape[2] * dz) : oorigin[0,2] : dz,
    ]  # pylint: disable = invalid-name
    volume = OArrayDicom
    volume = np.flip(OArrayDicom,axis=2)  # need to swap two axis and flip z since the axis must be increasing
    volume = np.swapaxes(volume, axis1=0, axis2=1)

    return x, y, z, dx, dy, dz, volume


