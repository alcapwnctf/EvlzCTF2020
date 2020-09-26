FROM ubuntu:18.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd 

#add user
RUN adduser --disabled-password --gecos '' malaria

#securityRestrictions
RUN chown -R root:malaria /home/malaria/
RUN chmod 750 /home/malaria
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/malaria/

COPY fake_flag /
RUN chown root:malaria /fake_flag
RUN chmod 440 /fake_flag

COPY malaria /home/malaria
RUN chmod +x /home/malaria/malaria
COPY flag.txt /home/malaria

RUN chown root:malaria /home/malaria/flag.txt
RUN chmod 440 /home/malaria/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
