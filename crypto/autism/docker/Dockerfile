FROM ubuntu:20.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' autism

#securityRestrictions
RUN chown -R root:autism /home/autism/
RUN chmod 750 /home/autism
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/autism/

COPY autism /home/autism
RUN chmod +x /home/autism/autism
COPY flag.txt /home/autism

RUN chown root:autism /home/autism/flag.txt
RUN chmod 440 /home/autism/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
