all: update-depends build-hyena build-cpp build-java
	@python3 run_test_script.py script

update-depends:
	@git submodule init
	@git submodule update
	@cd hyena-cpp && git checkout master && git pull
	@cd hyena-java && git checkout master && git pull
	@cd hyena     && git checkout master && git pull

build-cpp:
	@mkdir -p hyena-cpp/build && \
		cd hyena-cpp/build && \
		cmake .. && \
		make -s

build-hyena:
	@cd hyena/hyena-api; \
		cargo build --features=parse_msg --bin parse_msg; \
		cargo build --features=gen_test_out --bin gen_test_out

build-java:
	@cd hyena-java; \
		./gradlew gentestJar; \
		./gradlew parsemsgJar

.PHONY: clean
clean: clean-cpp clean-hyena clean-java
	@rm -f output.bin

clean-cpp:
	@rm -rf hyena-cpp/build

clean-hyena:
	@cd hyena/hyena-java; \
		cargo clean

clean-java:
	@cd hyena-java; \
		./gradlew clean
