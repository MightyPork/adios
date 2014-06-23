SOURCES = src/adios.py LICENSE

build: $(SOURCES)
	@./pack.sh -n

rel: $(SOURCES)
	@./pack.sh

setv:
	@./pack.sh -v $(v)
	
clean:
	@find ./build -type f \! -name '.gitignore' -delete
	@rm -rf ./tmp
	
