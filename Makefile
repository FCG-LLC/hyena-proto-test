all: build-hyena build-cpp build-java
	@python3 run_test_script.py script

build-cpp:
	@mkdir -p hyena-cpp/build && \
		cd hyena-cpp/build && \
		cmake .. && \
		make -s

build-hyena:
	@cd hyena-edge/hyena-api; \
		cargo build --features=parse_msg --bin parse_msg; \
		cargo build --features=gen_test_out --bin gen_test_out

build-java:
	@cd hyena-api; \
		./gradlew gentestJar

.PHONY: clean
clean: clean-cpp clean-hyena
	@rm -f output.bin

clean-cpp:
	@rm -rf hyena-cpp/build

clean-hyena:
	@cd hyena-edge/hyena-api; \
		cargo clean
