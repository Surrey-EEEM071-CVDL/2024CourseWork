#!/bin/bash

STUDENT_ID=kn00794 STUDENT_NAME="Jane Doe" python main.py \
-s veri \
-t veri \
-a mobilenet_v3_small \
--root /content \
--height 224 \
--width 224 \
--test-batch-size 100 \
--evaluate \
--save-dir logs/mobilenet_v3_small-veri \
--load-weights logs/mobilenet_v3_small-veri/model.pth.tar-2
