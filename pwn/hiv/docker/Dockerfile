FROM ubuntu:18.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' hiv

#securityRestrictions
RUN chown -R root:hiv /home/hiv/
RUN chmod 750 /home/hiv
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/hiv/

COPY hiv /home/hiv
RUN chmod +x /home/hiv/hiv
COPY flag.txt /home/hiv

RUN chown root:hiv /home/hiv/flag.txt
RUN chmod 440 /home/hiv/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
