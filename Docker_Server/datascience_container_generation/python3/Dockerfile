#!/usr/bin/env bash

FROM dataquestio/ubuntu-base

# Export env settings
ENV TERM=xterm
ENV LANG en_US.UTF-8

# Use apt to install the basics
RUN apt-get update -y && apt-get install build-essential -y
# We've decided to use cron
RUN apt-get -y install -qq --force-yes cron

# These are our real requirements once the base system is ready
ADD apt-packages.txt /tmp/apt-packages.txt
RUN xargs -a /tmp/apt-packages.txt apt-get install -y

# This image uses pip in a virtual environment. It's important to note
#	the location of the install for calling scripts externally
#	and hoping to access the correct version of python!
RUN pip install virtualenv
RUN /usr/local/bin/virtualenv /opt/ds --distribute --python=/usr/bin/python3

# Temporarily put our requirements file in the tmp folder of the image
ADD /requirements/ /tmp/requirements

# Run pip in three phases against our requirements
RUN /opt/ds/bin/pip install -r /tmp/requirements/pre-requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/post-requirements.txt

# Add a user. The uid and gid are set to 500 for AWS.
RUN useradd --create-home --home-dir /home/ds --shell /bin/bash ds
RUN usermod -u 500 ds
RUN groupmod -g 500 ds
RUN chown -R ds /opt/ds
RUN adduser ds sudo

# This is the script that we will run by default
ADD run_ipython.sh /home/ds
RUN chmod +x /home/ds/run_ipython.sh
RUN chown ds /home/ds/run_ipython.sh

# Cron stuff
RUN chown -R ds /var
RUN mkdir -p /var/cron.d
ADD Foxy_daily_run.sh /var/cron.d/
ADD Foxy_daily_run /var/cron.d/
RUN chmod +x /var/cron.d/Foxy_daily_run.sh
RUN chmod 0644 /var/cron.d/Foxy_daily_run
RUN touch /var/log/cron.log
RUN crontab /var/cron.d/Foxy_daily_run
#RUN touch /var/log/cron.log

# Setup the nginx web server
ADD http-default /etc/nginx/sites-enabled/default
# do we need to chmod and chown 'default'?
ADD .bashrc.template /home/ds/.bashrc


EXPOSE 8888
RUN usermod -a -G sudo ds
RUN echo "ds ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ds
RUN mkdir -p /home/ds/notebooks
ENV HOME=/home/ds
ENV SHELL=/bin/bash
ENV USER=ds
VOLUME /home/ds/notebooks
WORKDIR /home/ds/notebooks

CMD ["/home/ds/run_ipython.sh"]
CMD ["python /home/ds/notebooks/Backend/endpoints.py &"]

CMD ["cron && tail -f /var/log/cron.log"]
