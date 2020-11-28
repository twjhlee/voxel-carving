from PIL import Image, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import linecache
import glob
import open3d as o3d

def create_mask(img_filepath, parameter_file, angle_file, num):
	'''
	Parameters: img_filepath (string)-- file path of img
		    parameter_file (string)-- camera parameter file path
		    angle_file (string)-- camera angle parameter file path
		    num (int)-- img number, used to refer which line of parameter files contains camera configuration info for snapshot
	Returns: tuple of...
		 1) img-- mask as open3d image
		 2) open3d pinhole camera params object
		 	intrinsic camera matrix (K)
		 	extrinsic camera matrix (R|t) with extra row from identity matrix to make a 4x4 matrix
	'''
	img = Image.open(img_filepath).convert('1').filter(ImageFilter.BLUR).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MinFilter)
	#plt.imshow(img)
	#plt.show()
	img = np.asarray(img, dtype='float32')
	
	parameter_str = linecache.getline(parameter_file, num + 1).split()[1:]
	angle_str = linecache.getline(angle_file, num).split()[:-1]

	K = np.array([[float(parameter_str[0]), float(parameter_str[1]), float(parameter_str[2])], [float(parameter_str[3]), float(parameter_str[4]), float(parameter_str[5])], [float(parameter_str[6]), float(parameter_str[7]), float(parameter_str[8])]]);
	R = np.array([[float(parameter_str[9]), float(parameter_str[10]), float(parameter_str[11])], [float(parameter_str[12]), float(parameter_str[13]), float(parameter_str[14])], [float(parameter_str[15]), float(parameter_str[16]), float(parameter_str[17])]]);
	t = np.array([[float(parameter_str[18])], [float(parameter_str[19])], [float(parameter_str[20])]]);
	extrinsic = np.vstack((np.hstack((R, t)), np.array([[0.0, 0.0, 0.0, 1.0]], dtype='float32')))

	camera_params = o3d.camera.PinholeCameraParameters()	
	camera_params.extrinsic = extrinsic
	camera_params.intrinsic.set_intrinsics(img.shape[1], img.shape[0], K[0,0], K[1,1], K[0,2], K[1,2])
	return (o3d.geometry.Image(img), camera_params)

def carve_sides(dir, param_file, angle_file):
	'''
	Parameters: dir (string)-- directory of datafiles
		    param_file (string)-- string of camera parameters filepath
		    angle_file(string)-- string of camera angles filepath
	Returns: carved voxelspace
	'''
	print("creating voxel space...")
	voxel_grid = o3d.geometry.VoxelGrid.create_dense(origin=[320,320,320], color=[1,0,1], voxel_size=1, width =640, height =640, depth =640)
	print("created voxel space!")
	
	file_num = 1
	for img_file in sorted(glob.glob(dir + '*.png')):
		(img, params) = create_mask(img_file, param_file, angle_file, file_num)
		voxel_grid.carve_silhouette(img, params)
		file_num = file_num + 1
		
		print(file_num)
		o3d.visualization.draw_geometries([voxel_grid])

carve_sides('./temple/','./temple/temple_par.txt', './temple/temple_ang.txt')
