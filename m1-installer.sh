# some additional dependencies needed on m1 mac
brew install cmake
brew install rust

# haystack installation
GRPC_PYTHON_BUILD_SYSTEM_ZLIB=true 
pip install -r requirements.txt