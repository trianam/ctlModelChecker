#!/bin/sh
rm -fR *.pyc *~ __pycache__
cd Slides
rm -fR auto *.aux *.log *.toc *.nav *.out *.snm *.vrb img/*-converted-to.*
cd ..
