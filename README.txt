Requirements : 
	- python 3.6.0
	- opencv-contrib-python==3.3.0.10
		(pip install opencv-contrib-python==3.3.0.10)
	- scipy==0.18.1
		(pip install scipy==1.1.0)

How to use : 
	- python findCornersHarris.py
or :
	- python findCornersShitomasi.py

	This commands will iterate over the images in the directory img. 
	You can change the default images if you want(piece border is defined with alpha channel)

Interpret results : 
	after executing the scripts, you will get new images in folder resultHarris or resultShiTomasi depending on the script you used.
	Each image will be classified in one of the folder corresponding to the feature of the piece.
	in Harris, each side of the piece will be colored in another color.
	in ShiTomasi piece's corners will be printed in white and sides will be red or blue.
	And it's possible to observe precision because piece's contour is in green.
