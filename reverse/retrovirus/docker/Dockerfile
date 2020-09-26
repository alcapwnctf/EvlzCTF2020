FROM ubuntu:20.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' retrovirus

#securityRestrictions
RUN chown -R root:retrovirus /home/retrovirus/
RUN chmod 750 /home/retrovirus
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/retrovirus/

COPY retrovirus /home/retrovirus
RUN chmod +x /home/retrovirus/retrovirus
COPY flag.txt /

RUN chown root:retrovirus /flag.txt
RUN chmod 440 /flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
