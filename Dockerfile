FROM debian:wheezy
MAINTAINER jj
RUN useradd hacker
RUN DBEIAN_FRONTEND=noninteractive apt-get update && apt-get install wget python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
RUN mkdir /app/
ADD . /app/
EXPOSE 8080
WORKDIR /app/
RUN pip install -r /app/requirements.txt && chown -R hacker:hacker /app/
USER hacker
CMD /app/run.py 
