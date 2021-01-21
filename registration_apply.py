import argparse
import os
import sys
sys.path.append('C:\Program Files\GDCM 2.8\lib')
import pydicom
from PIL import *
import subprocess
# import gdcm
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import struct






#axial visualization and scrolling
def multi_slice_viewer_axial(volume):
    # remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[2] // 2
    print(ax.index)
    ax.imshow(volume[:,:,ax.index],aspect='auto')
    ax.set_title("slice="+ str(ax.index))
    fig.suptitle('Axial view', fontsize=16)
    fig.canvas.mpl_connect('key_press_event', process_key_axial)



def process_file(planname,regname,outname,proc_key):
    dataset = pydicom.dcmread(regname, force=True)

    #Rigid registration
    # print(dataset[0x0070,0x0308])
    # print(dataset[0x0070,0x0308].VM)
    # print(dataset[0x0070,0x0308][0])
    print(dataset[0x0070,0x0308][1][0x0070,0x0309][0][0x0070,0x030a][0])
    reg_type = dataset[0x0070, 0x0308][1][0x0070, 0x0309][0][0x0070, 0x030a][0][0x0070, 0x030c].value
    M = np.reshape(np.asarray(dataset[0x0070, 0x0308][1][0x0070, 0x0309][0][0x0070, 0x030a][0][0x3006, 0x00c6].value),(4,4))
    Minv = np.linalg.inv(M)
    print(reg_type,M,Minv)
    
    


    dataset2 = pydicom.dcmread(planname, force=True)  # now we load the plan dicom and apply the registration

    # print('Printing the UIDs')
    list_edit_meta=[(hex(0x0002),hex(0x0003))]
    list_edit=[(hex(0x0008),hex(0x0018)),(hex(0x0020),hex(0x000e))]

    for item in list_edit_meta:
        # print(dataset2.file_meta[item].value)
        tmp_split=str(dataset2.file_meta[item].value).split(sep='.')
        last_num=int(tmp_split[-1])
        separator='.'
        last_num=last_num+1
        tmp_split.pop(-1)
        tmp_split.append(str(last_num))
        updt_num=separator.join(tmp_split)
        dataset2.file_meta[item].value=updt_num
        # print(dataset2.file_meta[item].value)

    for item in list_edit:
        # print(dataset2[item].value)
        tmp_split=str(dataset2[item].value).split(sep='.')
        last_num=int(tmp_split[-1])
        separator='.'
        last_num=last_num+1
        tmp_split.pop(-1)
        tmp_split.append(str(last_num))
        updt_num=separator.join(tmp_split)
        dataset2[item].value=updt_num
        # print(dataset2[item].value)





    for elem in dataset2[0x300A, 0x0230][0][0x300A, 0x0280]:
        for pos in elem[0x300A, 0x02D0]:
            x, y, z = pos[0x300A, 0x02D4].value
            # print(pos[0x300A, 0x02D4].value)
            B=np.asarray([x,y,z,1])
            if proc_key==1:
                A = np.matmul(Minv,B)
            else:
                A = np.matmul(B,M)

            pos[0x300A, 0x02D4].value = [A[0],A[1],A[2]]
            # print(pos[0x300A, 0x02D4].value)


    dirname = os.path.dirname(planname)
    if outname is not None:
        dataset2.save_as(dirname + "/" + outname + ".dcm")  # this is working fine
        print('Modified plan written to',dirname + "/" + outname + ".dcm")



    # #Deformable registration
    # print(dataset[0x0064,0x0002].VM)
    # for i,elem in enumerate(dataset[0x0064,0x0002]):
    #     print(i,elem)
    #     # if (0x0070, 0x0309) in elem:
    #     #     print(elem[0x0070, 0x0309][0])
    #     if (0x0064, 0x0005) in elem:
    #         dX=[]
    #         dY=[]
    #         dZ=[]
    #         A=[]
    #         image_pos = np.asarray(elem[0x0064, 0x0005][0][0x0020, 0x0032].value)
    #         image_orient = np.asarray(elem[0x0064, 0x0005][0][0x0020, 0x0037].value)
    #         grid_dims = np.asarray(elem[0x0064, 0x0005][0][0x0064, 0x0007].value)
    #         grid_res = np.asarray(elem[0x0064, 0x0005][0][0x0064, 0x0008].value)
    #         grid_data = elem[0x0064, 0x0005][0][0x0064, 0x0009].value
    #         print(len(grid_data))
    #         for i in range(0,len(grid_data),4):
    #             A.append( struct.unpack('f',grid_data[i:i + 4]))
    #
    #         A=np.asarray(A)
    #         for ii in range(0,len(A),3):
    #             dX.append(A[ii])
    #             dY.append(A[ii+1])
    #             dZ.append(A[ii+2])
    #
    #
    #         dX=np.reshape(np.asarray(dX),(grid_dims[2],grid_dims[1],grid_dims[0]))
    #         dY=np.reshape(np.asarray(dY),(grid_dims[2],grid_dims[1],grid_dims[0]))
    #         dZ=np.reshape(np.asarray(dZ),(grid_dims[2],grid_dims[1],grid_dims[0]))
    #
    #
    #         fig, ax = plt.subplots()
    #         ax.volume = dX
    #         ax.index = dX.shape[2] // 2
    #         print(ax.index)
    #         ax.imshow(dX[:, :, ax.index], aspect='auto')
    #         ax.set_title("slice=" + str(ax.index))
    #         fig.suptitle('dX', fontsize=16)
    #
    #         fig, ax = plt.subplots()
    #         ax.volume = dY
    #         ax.index = dY.shape[2] // 2
    #         print(ax.index)
    #         ax.imshow(dY[:, :, ax.index], aspect='auto')
    #         ax.set_title("slice=" + str(ax.index))
    #         fig.suptitle('dY', fontsize=16)
    #
    #         fig, ax = plt.subplots()
    #         ax.volume = dZ
    #         ax.index = dZ.shape[2] // 2
    #         print(ax.index)
    #         ax.imshow(dZ[:, :, ax.index], aspect='auto')
    #         ax.set_title("slice=" + str(ax.index))
    #         fig.suptitle('dZ', fontsize=16)
    #
    #         plt.show()
    #
    #
    #     if (0x0064, 0x000f) in elem: #pre-deformation transform
    #         regPreM = elem[0x0064, 0x000f][0][0x3006, 0x00c6]
    #         print(regPreM)
    #
    #     if (0x0064, 0x0010) in elem: #post-deformation transform
    #         regPostM = elem[0x0064, 0x0010][0][0x3006, 0x00c6]
    #         print(regPostM)
    #
    #
    #
    # # multi_slice_viewer_axial(ArrayDicom)
    # # multi_slice_viewer_saggital(ArrayDicom)
    # # multi_slice_viewer_coronal(ArrayDicom)
    # # plt.show(block=True)









if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument("-p", "--plan", help="path to plan file",required=True)
    requiredNamed.add_argument("-r", "--registration", help="path to plan file",required=True)
    parser.add_argument("-o","--output",type=str,help="output plan file name, the file will be located in the same folder as the original, in DICOM format")
    parser.add_argument("-i","--inverse",help="if this key is enabled the inverse transform is applied to the plan",action='store_true')
    args = parser.parse_args()  # pylint: disable = invalid-name

    # while True:  # example of infinite loops using try and except to catch only numbers
    #     line = input('Are the files compressed [yes(y)/no(n)]> ')
    #     try:
    #         ##        if line == 'done':
    #         ##            break
    #         poption = str(line.lower())
    #         if poption.startswith(('y', 'yeah', 'yes', 'n', 'no', 'nope')):
    #             break
    #
    #     except:
    #         print('Please enter a valid option:')


    if args.plan and args.registration:
        planname = args.plan  # pylint: disable = invalid-name
        regname = args.registration  # pylint: disable = invalid-name
        if args.output:
            outf = args.output
            if args.inverse:
                process_file(planname, regname, outf, 1)
            else:
                process_file(planname, regname, outf, 0)

        else:
            if args.inverse:
                process_file(planname, regname, None, 1)
            else:
                process_file(planname, regname, None, 0)




