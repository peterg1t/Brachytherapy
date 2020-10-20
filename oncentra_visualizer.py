#############################START LICENSE##########################################
# Copyright (C) 2019 Pedro Martinez
#
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU Affero General Public License as published
# # by the Free Software Foundation, either version 3 of the License, or
# # (at your option) any later version (the "AGPL-3.0+").
#
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# # GNU Affero General Public License and the additional terms for more
# # details.
#
# # You should have received a copy of the GNU Affero General Public License
# # along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# # ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
# # Affero General Public License. These additional terms are Sections 1, 5,
# # 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
# # where all references to the definition "License" are instead defined to
# # mean the AGPL-3.0+.
#
# # You should have received a copy of the Apache-2.0 along with this
# # program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.
#############################END LICENSE##########################################

"""
 Script name: oncentra_visualizer.py

 Description: Integrated tool for visualization of Oncentra structure, plan and dose files

 Example usage: python oncentra_visualizer -s "/structure file/" -p "/plan file/" -d "/dose file/"

 Author: Pedro Martinez
 pedro.enrique.83@gmail.com
 5877000722
 Date:2019-07-18

"""


import argparse
import os
import csv
from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt
import oncdose
import oncplan
import oncstruct
import oncimg

os.environ["ETS_TOOLKIT"] = "qt4"


parser = argparse.ArgumentParser()
# parser.add_argument('structure',type=str,help="Input the structure file")
parser.add_argument(
    "-s",
    "--structure",
    nargs="?",
    type=argparse.FileType("r"),
    help="structure file, in DICOM format",
)
parser.add_argument(
    "-p",
    "--plan",
    nargs="?",
    type=argparse.FileType("r"),
    help="plan file, in DICOM format",
)
parser.add_argument(
    "-d",
    "--dose",
    nargs="?",
    type=argparse.FileType("r"),
    help="dose file, in DICOM format",
)
parser.add_argument(
    "-if",
    "--file",
    nargs="?",
    type=argparse.FileType("r"),
    help="image file, in DICOM format",
)
parser.add_argument(
    "-id",
    "--directory",
    help="image directory, in DICOM format",
)
args = parser.parse_args()

mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0.0, 0.0, 0.0))
scene = mlab.gcf().scene
scene.renderer.use_depth_peeling = 1


# using matplotlib3d
fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))


if args.structure:
    structname = args.structure
    print(structname.name)
    # using mayavi
    elem_data = oncstruct.process_file(structname.name)
    print('elem_data',elem_data[0,:], np.shape(elem_data),type(elem_data))
    # with open("test.csv","w+") as my_csv:            # writing the file as my_csv
    #     csvWriter = csv.writer(my_csv,delimiter=',')  # using the csv module to write the file
    #     csvWriter.writerows(elem_data)
    # using matplotlib
    # elem_data = oncstruct.process_file(structname.name, fig, ax)


if args.dose:
    dosename = args.dose
    print(dosename.name)
    x, y, z, dx, dy, dz, volume = oncdose.process_file(dosename.name)
    # using mayavi
    mlab.volume_slice(x, y, z, volume, plane_orientation="z_axes")
    # mlab.contour3d(x,y,z,volume,contours=15,opacity=1)
    mlab.colorbar(title="Dose [cGy]", orientation="vertical")


if args.file:
    filename = args.file
    print(filename.name)
    x, y, z, dx, dy, dz, volume = oncimg.process_file(filename.name)
    # using mayavi

    mlab.volume_slice(x, y, z, volume, plane_orientation="z_axes")
    # mlab.contour3d(x,y,z,volume,contours=15,opacity=1)
    mlab.colorbar(title="Pixel amplitude [a.u.]", orientation="vertical")

if args.directory:
    dirname = args.directory
    print(dirname)
    x, y, z, dx, dy, dz, volume = oncimg.process_directory(dirname)
    # using mayavi
    mlab.volume_slice(x, y, z, volume, plane_orientation="z_axes")
    # mlab.contour3d(x,y,z,volume,contours=15,opacity=1)
    mlab.colorbar(title="Pixel amplitude [a.u.]", orientation="vertical")

if args.plan:
    planname = args.plan
    print(planname.name)
    xs, ys, zs, ts = oncplan.process_file(planname.name)
    # using mayavi
    mlab.points3d(xs, ys, zs, ts)


ax = mlab.axes(nb_labels=8)
ax.axes.font_factor = 1

mlab.show()
