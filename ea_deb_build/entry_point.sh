export CC_COMPILER=gcc
export CXX_COMPILER=g++
export CMAKE_CC_COMPILER=gcc
export CMAKE_CXX_COMPILER=g++
export CXX=g++
export CC=gcc

gcc --version
g++ --version

for dir_name in eacirc CryptoStreams
do
    cd $dir_name
    mkdir -p build && cd build
    CC=$CC_COMPILER CXX=$CXX_COMPILER cmake .. -DCMAKE_BUILD_TYPE=Release
    # make -j8 ## allow this line to build all repositories, but it takes long time
    cd ~
done

tail -f /dev/null
