# Build image for EACirc tools - should contain everything

# update debian version based on metacentrum version
FROM debian

MAINTAINER Karel Kubicek "karel.kubicek@mail.muni.cz"

# install newest gcc, cmake, openssl
RUN 	apt-get update -qqy && \
	apt-get install -qqy \
	sudo gcc g++ cmake libssl-dev git python3 && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# root is no longer needed
# Add normal user with passwordless sudo
RUN useradd eacuser --shell /bin/bash --create-home \
  && usermod -a -G sudo eacuser \
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers \
  && echo 'eacuser:secret' | chpasswd
USER eacuser
WORKDIR /home/eacuser
RUN cd /home/eacuser

# clone all EAC repositories

RUN git clone https://github.com/crocs-muni/eacirc --recursive
RUN git clone https://github.com/crocs-muni/eacirc --branch=dev --recursive eacirc-dev
RUN git clone https://github.com/crocs-muni/eacirc-streams --recursive
RUN git clone https://github.com/crocs-muni/eacirc-streams --branch=dev --recursive eacirc-streams-dev
RUN git clone https://github.com/crocs-muni/eacirc-utils

# run entrypoint with build steps
ADD ./entry_point.sh /home/eacuser/entry_point.sh
ENTRYPOINT /home/eacuser/entry_point.sh

