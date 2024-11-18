TEMPLATES = {
	"CMakeLists.txt": """
cmake_minimum_required(VERSION 3.15)
project(%{PROJECT_NAME} VERSION %{PROJECT_VERSION} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic -O2")

file(GLOB_RECURSE SOURCES src/*.cpp)

add_executable(${PROJECT_NAME} ${SOURCES})

target_link_libraries(${PROJECT_NAME}
	glfw ${GLFW_LIBRARIES} ${OPENGL_LIBRARY}
)

install(TARGETS ${PROJECT_NAME} DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
	""",
	".clang-format": """
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120
	""",
	"build.sh": """
#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project information

BUILD_DIR="build"

# Functions
function print_header() {
	echo -e "${YELLOW}#######################################################################${NC}"
	echo -e "${YELLOW}### ${1}${NC}"
	echo -e "${YELLOW}#######################################################################${NC}"
}

function print_step() {
	currdate=$(date +"%Y-%m-%d %H:%M:%S")
	echo -e "${currdate} ${BLUE}[ * ] ${1}${NC}"
}

function print_debug() {
	currdate=$(date +"%Y-%m-%d %H:%M:%S")
	echo -e "${currdate} ${PURPLE}[ * ] ${1}${NC}"
}

function print_success() {
	currdate=$(date +"%Y-%m-%d %H:%M:%S")
	echo -e "${currdate} ${GREEN}[ ✓ ] ${1}${NC}"
}

function print_error() {
	currdate=$(date +"%Y-%m-%d %H:%M:%S")
	echo -e "${currdate} ${RED}[ ✗ ] ${1}${NC}"
}

currdate=$(date +"%Y-%m-%d %H:%M:%S")
clear

print_header "Cleaning up previous build"
if [ -d "$BUILD_DIR" ]; then
	print_step "Removing $BUILD_DIR directory..."
	rm -rf "$BUILD_DIR"
	print_success "Removed $BUILD_DIR directory."
else
	print_success "No previous build found."
fi

# Create build directory
print_header "Creating build directory"
print_step "Creating $BUILD_DIR directory..."
mkdir -p "$BUILD_DIR"
print_success "Created $BUILD_DIR directory."

# Configure the project
print_header "Configuring the project"
print_step "Running CMake in $BUILD_DIR..."
cd "$BUILD_DIR"

cmake ..

if [ $? -eq 0 ]; then
	print_success "CMake configuration completed successfully."
else
	print_error "CMake configuration failed."
	exit 1
fi

# Build the project
print_header "Building the project"
print_step "Building the project in $BUILD_DIR..."
make
if [ $? -eq 0 ]; then
	print_success "Project build completed successfully."
else
	print_error "Project build failed."
	exit 1
fi

# Install the project
print_header "Installing the project"
print_step "Installing the project..."
sudo make install
if [ $? -eq 0 ]; then
	print_success "Project installation completed successfully."
else
	print_error "Project installation failed."
	exit 1
fi

print_header "Build completed successfully"
echo -e "${CYAN}The project has been built and installed.${NC}"
echo "Build dir: build/"
""",
}
