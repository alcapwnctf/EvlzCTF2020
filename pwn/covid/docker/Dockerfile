FROM ubuntu:16.04
#installation

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd

#add user
RUN adduser --disabled-password --gecos '' easycovid

#securityRestrictions
RUN chown -R root:easycovid /home/easycovid/
RUN chmod 750 /home/easycovid
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/easycovid/

COPY easycovid /home/easycovid
RUN chmod +x /home/easycovid/easycovid
COPY flag.txt /home/easycovid

RUN chown root:easycovid /home/easycovid/flag.txt
RUN chmod 440 /home/easycovid/flag.txt

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337