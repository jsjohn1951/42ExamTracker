FROM debian:bookworm-slim

USER root

# ! noninteractive - zero interaction while installing or upgrading with apt
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y --no-install-recommends

RUN apt-get install \
	nodejs \
	npm \
	dialog \
	-y --no-install-recommends

COPY ./app /app
COPY ./scripts /scripts

# ! dialog - The default frontend for apt/apt-get under Debian/Ubuntu Linux.
ENV DEBIAN_FRONTEND=dialog