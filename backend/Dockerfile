FROM ubuntu:22.04

WORKDIR /app

# Installazione dei pacchetti necessari
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    git \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Specify the version of Gradle to install
ARG GRADLE_VERSION=8.0

# Install Gradle
RUN apt-get update && apt-get install -y wget unzip git && \
    wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip && \
    mkdir /opt/gradle && \
    unzip -d /opt/gradle gradle-${GRADLE_VERSION}-bin.zip && \
    rm gradle-${GRADLE_VERSION}-bin.zip && \
    ln -s /opt/gradle/gradle-${GRADLE_VERSION}/bin/gradle /usr/bin/gradle && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Clonazione della repository
RUN git clone https://github.com/lisa-analyzer/evm-lisa.git && \
    cd evm-lisa && \
    git checkout refactoring && \
    gradle assemble && \
    cp build/libs/evm-lisa-all.jar /app/evm-lisa/evm-lisa-all.jar && \
    cd .. && \
    rm -rf evm-lisa/


# Installazione delle dipendenze Python
COPY app/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia del codice
COPY . .

RUN ls -la
RUN ls -la app/

EXPOSE 9273

# Avvio dell'applicazione
CMD ["python3", "run.py"]