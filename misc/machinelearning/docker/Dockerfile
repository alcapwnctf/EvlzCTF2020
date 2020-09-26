FROM python:3-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd

#add user
RUN adduser --disabled-password --gecos '' adhd

#securityRestrictions
RUN chown -R root:adhd /home/adhd/
RUN chmod 750 /home/adhd
RUN export TERM=xterm

WORKDIR /home/adhd/

COPY app /home/adhd/
RUN chmod +x /home/adhd/main.py

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337