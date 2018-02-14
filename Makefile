all: build-hyena build-cpp
	@for script in `ls script`; do \
		python3 run_test_script.py script/$$script; \
	done

build-cpp:
	@mkdir -p hyena-cpp/build && \
		cd hyena-cpp/build && \
		cmake .. && \
		make -s

build-hyena:
	@cd hyena-edge/hyena-api; \
		cargo build --features=parse_msg --bin parse_msg; \
		cd ../..

.PHONY: clean
clean: clean-cpp clean-hyena
	@rm -f output.bin

clean-cpp:
	@rm -rf hyena-cpp/build

clean-hyena:
	@cd hyena-edge/hyena-api; \
		cargo clean
