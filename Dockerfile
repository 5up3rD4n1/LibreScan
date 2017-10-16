FROM labexperimental/debian:jessie

MAINTAINER LabExperimental <librescan@gmail.com>

ADD ./ /librescan

WORKDIR /librescan

RUN pip3 install -r src/requirements.txt

WORKDIR src/

RUN python3 setup.py

ENV LS_DEV_MODE=False

VOLUME /root/LibreScanProjects

EXPOSE 8080

CMD ["python3", "main.py", "web"]
