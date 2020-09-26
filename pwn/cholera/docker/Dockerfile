FROM ubuntu:16.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' cholera

#securityRestrictions
RUN chown -R root:cholera /home/cholera/
RUN chmod 750 /home/cholera
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/cholera/

COPY cholera /home/cholera
RUN chmod +x /home/cholera/cholera
COPY flag.txt /home/cholera

RUN chown root:cholera /home/cholera/flag.txt
RUN chmod 440 /home/cholera/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337