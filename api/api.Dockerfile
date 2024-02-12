FROM python:3-bullseye

USER root

# ! noninteractive - zero interaction while installing or upgrading with apt
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y --no-install-recommends \
	&& pip install --upgrade pip

RUN apt-get install \
	curl \
	ca-certificates \
	gcc \
	g++ \
	dialog \
	-y --no-install-recommends

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip3 install fastapi uvicorn websockets

COPY ./app /app
COPY ./scripts /scripts

# ! dialog - The default frontend for apt/apt-get under Debian/Ubuntu Linux.
ENV DEBIAN_FRONTEND=dialog