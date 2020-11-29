# Voxel Carving with Open3D in Python

### Data
Plaster reproduction of Temple of the Dioskouroi from Middlebury Multi-View Stereo Dataset (312 views sampled on a hemisphere) (https://vision.middlebury.edu/mview/data/)

Images captured on a Stanford Spherical Gantry (http://graphics.stanford.edu/projects/gantry/) and camera intrinsic and extrinsic matricies accompany each shot.

### Camera Calibration Parameters
We are given Matricies K containing info about the x and y focal length of the camera, along with the principal offset (x and y), R the rotation matrix, and t the translation vector along with our images.

**Description of Camera Intrinsic Matricies:**
http://ksimek.github.io/2013/08/13/intrinsic/

<a href="https://www.codecogs.com/eqnedit.php?latex=K&space;=&space;\left&space;(&space;\begin{array}{&space;c&space;c&space;c}&space;f_x&space;&&space;s&space;&&space;x_0&space;\\&space;0&space;&&space;f_y&space;&&space;y_0&space;\\&space;0&space;&&space;0&space;&&space;1&space;\\&space;\end{array}&space;\right&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K&space;=&space;\left&space;(&space;\begin{array}{&space;c&space;c&space;c}&space;f_x&space;&&space;s&space;&&space;x_0&space;\\&space;0&space;&&space;f_y&space;&&space;y_0&space;\\&space;0&space;&&space;0&space;&&space;1&space;\\&space;\end{array}&space;\right&space;)" title="K = \left ( \begin{array}{ c c c} f_x & s & x_0 \\ 0 & f_y & y_0 \\ 0 & 0 & 1 \\ \end{array} \right )" /></a>

*Focal Length* given by  <img src="https://latex.codecogs.com/gif.latex?f_z " /> , <img src="https://latex.codecogs.com/gif.latex?f_y " /> 

*Principal Point Offset* given by  <img src="https://latex.codecogs.com/gif.latex?x_0 " /> ,  <img src="https://latex.codecogs.com/gif.latex?y_0 " /> 

**Description of Camera Extrinsic Matricies:**
http://ksimek.github.io/2012/08/22/extrinsic/

<a href="https://www.codecogs.com/eqnedit.php?latex=[&space;R&space;\,&space;|\,&space;\boldsymbol{t}]&space;=&space;\left[&space;\begin{array}{ccc|c}&space;r_{1,1}&space;&&space;r_{1,2}&space;&&space;r_{1,3}&space;&&space;t_1&space;\\&space;r_{2,1}&space;&&space;r_{2,2}&space;&&space;r_{2,3}&space;&&space;t_2&space;\\&space;r_{3,1}&space;&&space;r_{3,2}&space;&&space;r_{3,3}&space;&&space;t_3&space;\\&space;\end{array}&space;\right]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[&space;R&space;\,&space;|\,&space;\boldsymbol{t}]&space;=&space;\left[&space;\begin{array}{ccc|c}&space;r_{1,1}&space;&&space;r_{1,2}&space;&&space;r_{1,3}&space;&&space;t_1&space;\\&space;r_{2,1}&space;&&space;r_{2,2}&space;&&space;r_{2,3}&space;&&space;t_2&space;\\&space;r_{3,1}&space;&&space;r_{3,2}&space;&&space;r_{3,3}&space;&&space;t_3&space;\\&space;\end{array}&space;\right]" title="[ R \, |\, \boldsymbol{t}] = \left[ \begin{array}{ccc|c} r_{1,1} & r_{1,2} & r_{1,3} & t_1 \\ r_{2,1} & r_{2,2} & r_{2,3} & t_2 \\ r_{3,1} & r_{3,2} & r_{3,3} & t_3 \\ \end{array} \right]" /></a>

*Rotational Matrix* given by - <img src="https://latex.codecogs.com/gif.latex?R " /> 
*Translational Vector* given by <img src="https://latex.codecogs.com/gif.latex?t " /> 

*Note: We add a fourth row in our extrinsic matrix to make it a 4x4 matrix. The fourth row corresponds to the 4th row of a 4x4 identity matrix.*

<a href="https://www.codecogs.com/eqnedit.php?latex=[&space;R&space;\,&space;|\,&space;\boldsymbol{t}]&space;=&space;\left[&space;\begin{array}{ccc|c}&space;r_{1,1}&space;&&space;r_{1,2}&space;&&space;r_{1,3}&space;&&space;t_1&space;\\&space;r_{2,1}&space;&&space;r_{2,2}&space;&&space;r_{2,3}&space;&&space;t_2&space;\\&space;r_{3,1}&space;&&space;r_{3,2}&space;&&space;r_{3,3}&space;&&space;t_3&space;\\&space;0&0&0&1&space;\end{array}&space;\right]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[&space;R&space;\,&space;|\,&space;\boldsymbol{t}]&space;=&space;\left[&space;\begin{array}{ccc|c}&space;r_{1,1}&space;&&space;r_{1,2}&space;&&space;r_{1,3}&space;&&space;t_1&space;\\&space;r_{2,1}&space;&&space;r_{2,2}&space;&&space;r_{2,3}&space;&&space;t_2&space;\\&space;r_{3,1}&space;&&space;r_{3,2}&space;&&space;r_{3,3}&space;&&space;t_3&space;\\&space;0&0&0&1&space;\end{array}&space;\right]" title="[ R \, |\, \boldsymbol{t}] = \left[ \begin{array}{ccc|c} r_{1,1} & r_{1,2} & r_{1,3} & t_1 \\ r_{2,1} & r_{2,2} & r_{2,3} & t_2 \\ r_{3,1} & r_{3,2} & r_{3,3} & t_3 \\ 0&0&0&1 \end{array} \right]" /></a>

### Open3D
We use Open3D to create a dense voxel grid using the `create_dense` function. We set the size of each voxel as follows...

<a href="https://www.codecogs.com/eqnedit.php?latex=Voxel&space;Size&space;=&space;\frac{Dimension_{Cubic&space;Voxel&space;Dense}}{max(pixels_{width},&space;pixels_{height})}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Voxel&space;Size&space;=&space;\frac{Dimension_{Cubic&space;Voxel&space;Dense}}{max(pixels_{width},&space;pixels_{height})}" title="Voxel Size = \frac{Dimension_{Cubic Voxel Dense}}{max(pixels_{width}, pixels_{height})}" /></a>

So for us, we used a 2x2x2 cubic voxel dense, the images we were given were 640 x 480. so the size of each voxel was 2/640 = 0.003125.

We also used Open3D to do the carving. To implement the carving we created a silhouette and grabbed the camera parameters for each image, and passed them to the `carve_silhouette` method.

(http://www.open3d.org/docs/0.8.0/python_api/open3d.geometry.VoxelGrid.html)

Finally we use `draw_geometries` to show the result of voxel carving. 
(http://www.open3d.org/docs/latest/python_api/open3d.visualization.html)

*Note: `draw_geometries` did not work on Mac with pip install of Open3D, it worked on Debian Linux though.*

### Results

![Alt Text](https://github.com/cranberrymuffin/voxel-carving/blob/main/results/Large%20GIF%20(802x626).gif)

