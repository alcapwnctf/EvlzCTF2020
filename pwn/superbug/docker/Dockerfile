FROM ubuntu:20.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' superbug

#securityRestrictions
RUN chown -R root:superbug /home/superbug/
RUN chmod 750 /home/superbug
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/superbug/

COPY superbug /home/superbug
RUN chmod +x /home/superbug/superbug
COPY flag.txt /home/superbug

RUN chown root:superbug /home/superbug/flag.txt
RUN chmod 440 /home/superbug/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
