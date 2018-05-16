FROM ubuntu:bionic

RUN apt-get update
RUN apt-get -y install openssh-client wget unzip curl make git \
    libnanomsg-dev cmake libcereal-dev libboost-dev libboost-log-dev \
    libcpputest-dev openjdk-8-jdk python3

# Install Gradle
ENV GRADLE_VERSION 2.12
ENV GRADLE_HOME /usr/local/gradle
ENV PATH ${PATH}:${GRADLE_HOME}/bin
ENV GRADLE_USER_HOME /gradle

WORKDIR /usr/local
RUN wget  https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip && \
    unzip gradle-$GRADLE_VERSION-bin.zip && \
    rm -f gradle-$GRADLE_VERSION-bin.zip && \
    ln -s gradle-$GRADLE_VERSION gradle && \
    echo -ne "- with Gradle $GRADLE_VERSION\n" >> /root/.built

# Install Rust
RUN curl https://sh.rustup.rs -sSf > /tmp/rustup-init.sh && sh /tmp/rustup-init.sh -y

# Install GCC
RUN apt-get -y install g++

# Prepare keys
COPY config/known_hosts /root/.ssh/
RUN echo "echo -e "\${HYENA_PRIVATE_KEY}" > ~/.ssh/id_rsa; chmod 0600 ~/.ssh/id_rsa" > /setup_ssh_key.sh
RUN chmod a+x /setup_ssh_key.sh

RUN mkdir /proto-test
WORKDIR /proto-test
COPY . /proto-test
COPY config/run_tests.sh /run_tests.sh

CMD ["/run_tests.sh"]
