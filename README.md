Task
There is an image located in the same folder as part1.py. In our case, it is a printed circuit board in gray tones. It must be disassembled into unconnected conductors. They are independent graphic objects.



Execution idea
First, we crop the image in a rectangular area by setting two points. Then we convert this image into a black-and-white image and write it to a 5.png file After that, we mark up the image with a standard function and divide it into disconnected areas. Each object is written to its own file. Their entire package is concentrated in the masks folder. This folder will be created next to the module.
This project is licensed by MIT.

