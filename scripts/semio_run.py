#!/usr/bin/python

import os
import argparse
import sys
import shlex
import subprocess

parser = argparse.ArgumentParser( description='Start semio components' )

parser.add_argument( "--no-rm", action="store_true", help="save image" )
parser.add_argument( "--nvidia", action="store_true", help="launch with support for nvidia cards; implies --display" )
parser.add_argument( "--display", action="store_true", help="launch with display support" )
parser.add_argument( "--usb", action="store_true", help="launch with USB support" )
parser.add_argument( "--ros", action="store_true", help="launch with ROS support" )
parser.add_argument( "--ros-master", help="set ros master hostname (default: master); implies --ros" )
parser.add_argument( "--repo", default='docker.semio.xyz:5000', help="set docker repo" )
parser.add_argument( "--variant", default='libsemio-ros:latest', help="set docker container variant" )
parser.add_argument( "-e", "--env", action="append", help="pass environment variables" )
parser.add_argument( "-d", "--docker-flag", action="append", help="pass docker flags (:flag=value)" )
parser.add_argument( "args", nargs=argparse.REMAINDER, help="args to pass" )

args = parser.parse_args()

cmd_list = [ 'docker', 'run', '-ti' ]

if not args.no_rm:
	cmd_list.append( '--rm' )

if args.nvidia:
	cmd_list[0] = 'nvidia-docker'
	args.display = True

if args.display:
	cmd_list.extend( '-e DISPLAY'.split() )
	cmd_list.extend( '-v /tmp/.X11-unix:/tmp/.X11-unix'.split() )

	if not args.nvidia:
		cmd_list.append( '--device=/dev/dri' )

if args.usb:
	cmd_list.append( '--device=/dev/bus/usb' )

if args.ros_master:
	cmd_list.extend( ( '-e ROS_MASTER_URI=http://' + args.ros_master + ':11311' ).split() )
	args.ros = True

if args.ros:
	cmd_list.append( '--net=ros' )

	if not args.ros_master:
		cmd_list.extend( '-e ROS_MASTER_URI=http://master:11311'.split() )

if args.usb or ( args.display and not args.nvidia ):
	cmd_list.append( '--privileged' )

if args.env:
	for env_arg in args.env:
		cmd_list.extend( ( '-e ' + env_arg ).split() )

if args.docker_flag:
	for docker_flag in args.docker_flag:
		cmd_list.extend( docker_flag[1:].split() )

cmd_list.append( args.repo + '/' + args.variant )

if args.display:
	FNULL = open(os.devnull, 'w')
	subprocess.check_call( [ 'xhost', '+' ], stdout=FNULL )

cmd_list.extend( shlex.split( ' '.join( args.args ) ) )

print '>> ' +  ' '.join( cmd_list )

subprocess.call( cmd_list )
