import os

for i in range(1,90):
    print(i)
    if i<10:
        os.system('python refine.py --dicom /Users/sungminlee/ServerFile/syd/LUNG3-0'+str(i)+' --volume /Users/sungminlee/ServerFile/slice/case'+str(i)+'.nii --seg /Users/sungminlee/ServerFile/slice/key'+str(i)+'.nii')
    else:
        os.system('python refine.py --dicom /Users/sungminlee/ServerFile/syd/LUNG3-' + str(i) + ' --volume /Users/sungminlee/ServerFile/slice/case' + str(i) + '.nii --seg /Users/sungminlee/ServerFile/slice/key' + str(i) + '.nii')