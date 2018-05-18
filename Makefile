HYENA_COMMIT ?= master
HYENA_CPP_COMMIT ?= master
HYENA_JAVA_COMMIT ?= master

all: show-variables update-depends build-hyena build-cpp build-java
	@python3 run_test_script.py script

update-depends:
	@git submodule init
	@git submodule update
	@cd hyena-cpp  && git checkout ${HYENA_CPP_COMMIT}  && git pull
	@cd hyena-java && git checkout ${HYENA_JAVA_COMMIT} && git pull
	@cd hyena      && git checkout ${HYENA_COMMIT}      && git pull

build-cpp:
	@mkdir -p hyena-cpp/build && \
		cd hyena-cpp/build && \
		cmake -DHYENA_DEBUG=OFF .. && \
		make -s

build-hyena:
	@cd hyena/hyena-api; \
		cargo build --features=parse_msg --bin parse_msg; \
		cargo build --features=gen_test_out --bin gen_test_out

build-java:
	@cd hyena-java; \
		./gradlew gentestJar; \
		./gradlew parsemsgJar

.PHONY: show-variables clean

show-variables:
	@echo -----
	@echo Using following commits/branches for tests
	@echo hyena:      ${HYENA_COMMIT}
	@echo hyena-cpp:  ${HYENA_CPP_COMMIT}
	@echo hyena-java: ${HYENA_JAVA_COMMIT}
	@echo -----

clean: clean-cpp clean-hyena clean-java
	@rm -f output.bin

clean-cpp:
	@rm -rf hyena-cpp/build

clean-hyena:
	@cd hyena/hyena-api; \
		cargo clean

clean-java:
	@cd hyena-java; \
		./gradlew clean
