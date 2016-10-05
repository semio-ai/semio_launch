cmake_minimum_required(VERSION 2.8.3)
project(semio_launch)

# find catkin dependencies
find_package(catkin REQUIRED)

# declare catkin package
catkin_package(
)

# add include directores of dependencies to header search path
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# mark other files for installation (e.g. launch and bag files, etc.)
install(
  DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
  FILES_MATCHING PATTERN "*.launch"
)

install(
  DIRECTORY config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
  FILES_MATCHING PATTERN "*.rviz"
)

install(
  DIRECTORY scripts/
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  USE_SOURCE_PERMISSIONS
  FILES_MATCHING PATTERN "*.py" PATTERN "*.sh"
)
