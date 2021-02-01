
pkg='paramak'
array=( 3.6 3.7 3.8 )

rm -rf /tmp/cbld

for i in "${array[@]}"
do
	conda-build . -c cadquery -c conda-forge --croot /tmp/cbld --python $i 
done


# # convert package to other platforms
platforms=( osx-64 linux-32 linux-64 win-32 win-64 )
# find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done
    
# done

find /tmp/cbld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload $file
done


# conda install -c giswqs paramak