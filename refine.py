import pydicom , os, argparse, glob, numpy as np , cv2 , tqdm
import SimpleITK as sitk , nibabel as nib , dicom2nifti as dn


parser = argparse.ArgumentParser()
parser.add_argument('--seg', metavar='FILENAME',help = 'input segmentation image file name', required=True )
parser.add_argument('--dicom', metavar='FILENAME',help = 'input dicom directory',required=True)
parser.add_argument('--volume', metavar='FILENAME',help = 'input image file name', required=True )
args = parser.parse_args()

files = os.listdir(args.dicom)
try: files.pop(files.index('.DS_Store'))
except : pass

files = sorted(files)

seq = []
dicom = []
for i in files:
    num = int(i[:i.index('.dcm')])
    data = pydicom.dcmread(args.dicom+'/'+ i)
    act_num = str(data[0x0020,0x0013])
    act_num = int(act_num[act_num.index('"')+1:act_num.rfind('"')])-1
    # if act_num>=89:
    #     act_num = act_num-2


    seq.append([act_num,num])
    dicom.append(act_num)

data= nib.load(args.volume)
img = data.get_fdata()
slices = img[:,:,:]
print(slices.shape)

seg = nib.load(args.seg)
seg = seg.get_fdata()
seg = seg[:,:,:]
print(seg.shape)

vol = np.empty(shape=slices.shape)
stack = np.empty(shape=slices.shape)

for i in seq:
    print(i)
print(len(seq))

dic, ni = zip(*seq)

print(min(dic),max(dic),len(dic))
print(min(ni),max(ni),len(ni))
# print(sorted(dic))



for dic , ni in seq :
    vol[:,:,dic] = slices[:,:,ni]
    stack[:,:,dic] = seg[:,:,ni]

reverse_stack = np.flip(stack ,2)

os.makedirs(os.path.dirname(args.volume)+args.dicom[args.dicom.rfind('/'):],exist_ok=True)

stack = stack.astype(np.int16,copy=False)
ni_img = nib.Nifti1Image(stack,affine=np.eye(4))
nib.save(ni_img,os.path.dirname(args.volume)+args.dicom[args.dicom.rfind('/'):]+'/refine_seg.nii')

vol = vol.astype(np.int16,copy=False)
raw_img = nib.Nifti1Image(vol,affine=np.eye(4))
nib.save(raw_img,os.path.dirname(args.volume)+args.dicom[args.dicom.rfind('/'):]+'/refine_raw.nii')

reverse = nib.Nifti1Image(reverse_stack,affine=np.eye(4))
nib.save(reverse,os.path.dirname(args.volume)+args.dicom[args.dicom.rfind('/'):]+'/refine_reverse_seg.nii')

