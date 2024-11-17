TEMPLATES = {
	"CMakeLists.txt": """
cmake_minimum_required(VERSION 3.15)
project(gl-learn VERSION 1.0 LANGUAGES CXX)

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
}
