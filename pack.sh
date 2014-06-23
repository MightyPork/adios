#!/bin/bash

__COLOR_BLACK='\033[30m'
__COLOR_BLACK2='\033[0;30;1m'
__COLOR_RED='\033[31m'
__COLOR_RED2='\033[0;31;1m'
__COLOR_GREEN='\033[32m'
__COLOR_GREEN2='\033[0;32;1m'
__COLOR_YELLOW='\033[33m'
__COLOR_YELLOW2='\033[0;33;1m'
__COLOR_BLUE='\033[34m'
__COLOR_BLUE2='\033[0;34;1m'
__COLOR_MAGENTA='\033[35m'
__COLOR_MAGENTA2='\033[0;35;1m'
__COLOR_CYAN='\033[36m'
__COLOR_CYAN2='\033[0;36;1m'
__COLOR_WHITE='\033[37m'
__COLOR_WHITE2='\033[0;37;1m'
__COLOR_RESET='\033[0m'

INCREL=1

function cecho {
	eval "a=\$__COLOR_$2"
	echo -e $a$1$__COLOR_RESET
}

while getopts ":nrv:" opt; do
	case $opt in

		n)
			cecho "Test build, _REL will not be incremented." YELLOW2
			INCREL=0
			;;

		v)
			vers=$OPTARG
			oldvers=$(cat _VERSION)
		
			if [[ "${vers}" != "${oldvers}" ]]; then
				echo $vers > _VERSION
				echo 1 > _REL
				cecho "Version set to $vers, rel counter reset to 1." YELLOW2
			else
				cecho "Version unchanged." RED2
			fi
			
			exit 0
		
			;;

		\?)
			cecho "Invalid option: -$OPTARG" RED2 >&2
			exit 1
			;;

		:)
			cecho "Option -$OPTARG requires an argument." RED2 >&2
			exit 1
			;;
	esac
done


# load version and rel from counter files
typeset -i REL=$(cat _REL)
VERSION=$(cat _VERSION)

# echo their current values
cecho "rel = ${REL}" BLUE
cecho "version = ${VERSION}" BLUE


# copy all stuff into tmp (clean tmp first)
mkdir -p tmp
rm -rf tmp/*
cp LICENSE tmp
cp src/adios.py tmp/adios


TAR="build/adios-${VERSION}-${REL}.tar.gz"
# build a tar of the stuff
tar cfz $TAR -C tmp LICENSE adios

# grab md5 of the tar
MD5=$(md5sum ${TAR} | cut -d ' ' -f 1)
cecho "MD5 = ${MD5}" BLUE



# increment release number if needed
if [ $INCREL = 1 ]; then
	cecho "Incrementing _REL $REL -> $(($REL + 1))." CYAN
	echo $(($REL + 1)) > _REL
fi

# generate PKGBUILD with the version and release.
sed -e "s/%rel/${REL}/g" -e "s/%version/${VERSION}/g" -e "s/%md5/${MD5}/g" PKGBUILD.tpl > build/PKGBUILD
