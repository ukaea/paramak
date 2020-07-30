#!/bin/bash# change the package name to the existing PyPi package you would like to build
pkg='paramak'
# adjust the Python versions you would like to build
array=( 3.5 3.6 3.7 3.8)echo "Building conda package ..."
cd ~
conda skeleton pypi $pkg
cd $pkg
wget https://conda.io/docs/_downloads/build1.sh
wget https://conda.io/docs/_downloads/bld.bat
cd ~# building conda packages
for i in "${array[@]}"
do
	conda-build --python $i $pkg
done# convert package to other platforms
cd ~
platforms=( osx-64 linux-32 linux-64 win-32 win-64 )
find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done    
done# upload packages to conda
find $HOME/conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
doneecho "Building conda package done!"