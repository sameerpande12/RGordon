##!/usr/bin/env bash

mkdir -p /home/sameerpande34/Desktop/Gordon/Test/Data$c
sudo docker run --name=gordon$c -d -v ~/Desktop/Gordon/Data:/home/tester/Gordon/Data --privileged -i -t 740d bash
sudo docker exec -i -t gordon$c bash
