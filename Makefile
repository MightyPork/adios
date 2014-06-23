
build: 
	mkdir -p ./build
	
	# make tarball
	tar cfz build/release.tar.gz LICENSE -C src adios.py
	
clean:
	# cleanup
	rm -rf build/*.tar.gz
	rm -rf *~
	
