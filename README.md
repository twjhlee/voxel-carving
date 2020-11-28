# Voxel Carving with Open3D in Python

### Data
Plaster reproduction of Temple of the Dioskouroi from Middlebury Multi-View Stereo Dataset (312 views sampled on a hemisphere) (https://vision.middlebury.edu/mview/data/)

Images captured on a Stanford Spherical Gantry (http://graphics.stanford.edu/projects/gantry/) and camera intrinsic and extrinsic matricies accompany each shot.

### Camera Calibration Parameters
We are given Matricies K containing info about the x and y focal length of the camera, along with the principal offset (x and y), R the rotation matrix, and t the translation matrix along with our images.

**Description of Camera Intrinsic Matricies:**
http://ksimek.github.io/2013/08/13/intrinsic/
$$
K = \left ( 
                \begin{array}{ c c c}
                f_x & s   & x_0 \\
                 0  & f_y & y_0 \\
                 0  & 0   & 1 \\
                \end{array}
            \right )
$$

*Focal Length* given by  $f_x$,  $f_y$
*Principal Point Offset* given by  $x_0$,  $y_0$

**Description of Camera Extrinsic Matricies:**
http://ksimek.github.io/2012/08/22/extrinsic/

$$
[ R \, |\, \boldsymbol{t}] = 
\left[ \begin{array}{ccc|c} 
r_{1,1} & r_{1,2} & r_{1,3} & t_1 \\
r_{2,1} & r_{2,2} & r_{2,3} & t_2 \\
r_{3,1} & r_{3,2} & r_{3,3} & t_3 \\
\end{array} \right]
$$

*Rotational Matrix* given by $R$
*Translational Vector* given by $t$

*Note: We add a fourth row in our extrinsic matrix to make it a 4x4 matrix. The fourth row corresponds to the 4th row of a 4x4 identity matrix.*
$$
[ R \, |\, \boldsymbol{t}] = 
\left[ \begin{array}{ccc|c} 
r_{1,1} & r_{1,2} & r_{1,3} & t_1 \\
r_{2,1} & r_{2,2} & r_{2,3} & t_2 \\
r_{3,1} & r_{3,2} & r_{3,3} & t_3 \\
0&0&0&1
\end{array} \right]
$$


### Open3D
We use Open3D to create a dense voxel grid using the `create_dense` function. We set the size of each voxel as follows...
$$
Voxel Size = \frac{Dimension_{Cubic Voxel Dense}}{max(pixels_{width}, pixels_{height})}
$$


So for us, we used a 2x2x2 cubic voxel dense, the images we were given were 640 x 480. so the size of each voxel was 2/640 = 0.003125.

We also used Open3D to do the carving. To implement the carving we created a silhouette and grabbed the camera parameters for each image, and passed them to the `carve_silhouette` method.

(http://www.open3d.org/docs/0.8.0/python_api/open3d.geometry.VoxelGrid.html)

Finally we use `draw_geometries` to show the result of voxel carving. 
(http://www.open3d.org/docs/latest/python_api/open3d.visualization.html)

*Note: `draw_geometries` did not work on Mac with pip install of Open3D, it worked on Debian Linux though.*

