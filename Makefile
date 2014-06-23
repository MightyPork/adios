
release: LICENSE src/adios.py
	mkdir -p build
	tar cfz build/release.tar.gz LICENSE -C src adios.py
