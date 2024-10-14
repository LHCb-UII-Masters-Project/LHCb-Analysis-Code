###############################################################################
# (c) Copyright 2000-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################


if( CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR )
  project(Upgrade2Selections)
  cmake_minimum_required(VERSION 3.9)

  find_package(ROOT REQUIRED COMPONENTS RIO Tree Matrix MathCore )

  set(RECO4D         FALSE    CACHE BOOL   "RECO4D")     # flag to use openmp for threading 
  add_library( Event SHARED src/uParticle.cpp src/uVertex.cpp src/TrackState.cpp src/uComposite.cpp )
  if ( RECO4D )
    target_compile_definitions( Event PRIVATE "RECO4D=1" )
  else()
    target_compile_definitions( Event PRIVATE "RECO4D=0" )
  endif()
  target_link_libraries( Event ROOT::RIO ROOT::Matrix ROOT::MathCore )
  target_include_directories(Event PUBLIC ${PROJECT_SOURCE_DIR}/include/ ${ROOT_INCLUDE_DIRS} )

  configure_file ("${PROJECT_SOURCE_DIR}/detail/Selections.py.in" "${CMAKE_BINARY_DIR}/Selections.py")

  ROOT_GENERATE_DICTIONARY(event_dict
    include/Event/uVertex.h
    include/Event/uComposite.h
    include/Event/uMCVertex.h
    include/Event/uMCParticle.h
    include/Event/uParticle.h
    include/Event/TrackState.h
    include/Event/uPi0.h
    LINKDEF include/Event/LinkDef.h
    MODULE Event )

  get_target_property( includes Event INCLUDE_DIRECTORIES )
  file(GLOB_RECURSE utils utils/*.cpp )
  foreach( file ${utils} )
    get_filename_component( Executable ${file} NAME_WE )
    add_executable(${Executable}${EXEC_EXTENSION} ${file})
    target_compile_options(${Executable}${EXEC_EXTENSION} PUBLIC -g3 -O3)
    target_link_libraries(${Executable}${EXEC_EXTENSION} PUBLIC Event event_dict ${ROOT_LIBRARIES} )
    target_include_directories(${Executable}${EXEC_EXTENSION} PRIVATE ${ROOT_INCLUDE_DIRS})
  endforeach() 

else() 
  gaudi_add_library( u2Event SOURCES src/uParticle.cpp src/uVertex.cpp src/TrackState.cpp
    LINK
    ROOT::Matrix
    ROOT::MathCore)

  gaudi_add_dictionary(u2EventDict
    HEADERFILES dict/dictionary.h
    SELECTION dict/selection.xml
    LINK u2Event)

  gaudi_add_module(U2Tuple 
    SOURCES src/MakeTuple.cpp
    LINK
    LHCb::TrackEvent
    LHCb::RecEvent
    LHCb::MCEvent
    u2Event
    Gaudi::GaudiAlgLib
    ROOT::RIO 
    ROOT::Tree
    )
endif() 
