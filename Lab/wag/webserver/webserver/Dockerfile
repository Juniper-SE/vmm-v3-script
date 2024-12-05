FROM alpine
MAINTAINER irzan "m.irzan@gmail.com"
RUN apk add --update --no-cache python3 py3-pip curl busybox-extras openssh
COPY . /workingdir
WORKDIR /workingdir
RUN pip install -r requirements.txt
RUN pip cache purge
EXPOSE  80
ENTRYPOINT ["python3"]
CMD ["webserver.py"]
