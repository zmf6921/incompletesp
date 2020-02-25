# File: benchmark.py
# Authors: Zack Fitzsimmons (zfitzsim@holycross.edu),
#          Martin Lackner (lackner@dbai.tuwien.ac.at)


import weakordersp
import os
import time


for i, filename in enumerate(os.listdir("toc")):
    print(str(i)+",", end="")
    start_time = time.time()
    weakordersp.testsp_file("toc/"+filename, 0)
    print(",%.2f" % (time.time() - start_time))
