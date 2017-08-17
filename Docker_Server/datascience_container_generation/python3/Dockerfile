#!/usr/bin/env bash

FROM dataquestio/ubuntu-base

# Export env settings
ENV TERM=xterm
ENV LANG en_US.UTF-8

RUN apt-get update -y && apt-get install build-essential -y
RUN apt-get -y install -qq --force-yes cron

ADD apt-packages.txt /tmp/apt-packages.txt
RUN xargs -a /tmp/apt-packages.txt apt-get install -y

RUN pip install virtualenv
RUN /usr/local/bin/virtualenv /opt/ds --distribute --python=/usr/bin/python3

ADD /requirements/ /tmp/requirements

RUN /opt/ds/bin/pip install -r /tmp/requirements/pre-requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/post-requirements.txt

RUN useradd --create-home --home-dir /home/ds --shell /bin/bash ds
RUN usermod -u 500 ds
RUN groupmod -g 500 ds
RUN chown -R ds /opt/ds
RUN adduser ds sudo

ADD run_ipython.sh /home/ds
RUN chmod +x /home/ds/run_ipython.sh
RUN chown ds /home/ds/run_ipython.sh

ADD run_endpoints.sh /home/ds
RUN chmod +x /home/ds/run_endpoints.sh
RUN chown ds /home/ds/run_endpoints.sh

RUN mkdir -p /var/cron.d
RUN chown -R ds /var
RUN chown -R ds /var/log
ADD Foxy_daily_run.sh /var/cron.d
ADD Foxy_daily_run /var/cron.d
RUN chmod +x /var/cron.d/Foxy_daily_run.sh
RUN chmod 0644 /var/cron.d/Foxy_daily_run
RUN /usr/bin/crontab /var/cron.d/Foxy_daily_run 
RUN touch /tmp/cron.log
RUN touch /tmp/DecayModel.log
RUN touch /tmp/BayesModel.log
RUN touch /tmp/LatestModel.log
RUN touch /tmp/GPModel.log

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

CMD ["/home/ds/run_ipython.sh","/usr/bin/crontab -u ds /var/cron.d/Foxy_daily_run", "sudo cron && tail -f /dev/null"]
#CMD ["/home/ds/run_ipython.sh","/usr/bin/crontab -u ds /var/cron.d/Foxy_daily_run", "sudo | service cron start && tail -f /dev/null"]
