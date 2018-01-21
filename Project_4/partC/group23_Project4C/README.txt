Dependencies: dlib, cv2(OpenCV3), imutils, imageio

This project uses dlib and OpenCV3 to detect faces using cnn.

To install dlib:
	- Download: http://dlib.net/files/dlib-19.7.tar.bz2
	- Extract the archive and cd into the directory
	- sudo python setup.py install (regular install)
	- python setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA (with GPU support)
The code was tested on a machine with a GPU and dlib was ran with the GPU.

Note that OpenCV3 has to be installed for seamlessClone to work.

imutils and image io can be installed by pip.

faceswap.py is the main method and it can be ran like this:

	python faceswap.py --video_background "<body_video_path>" --video_face "<face_video_path>" --output_name "<output_video_path>"

Alpha blending is included in the code but an alpha of 1 is used for better results from our experiment, which means alpha blending is disabled. To enable alpha blending, change the value on line 33 in faceswap.py.

A cnn-base face detector is also included in the code. We didn't use it because it didn't show dramatic improvement on face detection.


