FROM labexperimental/debian:jessie

MAINTAINER LabExperimental <librescan@gmail.com>

VOLUME /root/LibreScanProjects

VOLUME /root/.librescan

EXPOSE 8080

ADD ./ /api

WORKDIR /tmp

RUN python3 -m venv ~/.virtualenvs/librescan && \
    /bin/bash -c "source ~/.virtualenvs/librescan/bin/activate" && \
    pip install lupa --install-option='--no-luajit' && \
    chmod +x /api/misc/docker-entry.sh && \
    chmod +x /api/misc/chdkptp.sh && \
    sh /api/misc/chdkptp.sh

WORKDIR /api/librescan

RUN pip install -r requirements.txt && \
    python setup.py

ENV LS_DEV_MODE=False

ENTRYPOINT ["../misc/docker-entry.sh"]