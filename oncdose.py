"""
Script name: oncdose

Description: Tool for processing of Oncentra dose files

Author: Pedro Martinez
pedro.enrique.83@gmail.com
5877000722
Date:2019-05-10

"""


from mayavi import mlab

import numpy as np

import matplotlib.pyplot as plt

import pydicom


# def process_file(filename,ax,fig):
def process_file(filename):
    """This function process an Oncentra dose file  """
    # print('Starting dose calculation')
    dataset = pydicom.dcmread(filename)
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

    # for mayavi
    x, y, z = np.mgrid[
        origin[0] : origin[0] + (array_dicom.shape[2] * dx) : dx,
        origin[1] : origin[1] + (array_dicom.shape[1] * dy) : dy,
        origin[2] - (array_dicom.shape[0] * dz) : origin[2] : dz,
    ]  # pylint: disable = invalid-name
    volume = np.flip(
        np.swapaxes(array_dicom, axis1=0, axis2=2), axis=2
    )  # need to swap two axis and flip z since the axis must be increasing
    volume = np.swapaxes(volume, axis1=0, axis2=1)

    return x, y, z, dx, dy, dz, volume
