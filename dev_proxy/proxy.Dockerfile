FROM nginx:bookworm

# ! noninteractive - zero interaction while installing or upgrading with apt
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y --no-install-recommends

COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf 

# ! dialog - The default frontend for apt/apt-get under Debian/Ubuntu Linux.
ENV DEBIAN_FRONTEND=dialog