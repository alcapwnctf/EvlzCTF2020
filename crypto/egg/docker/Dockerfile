FROM python:3-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd

#add user
RUN adduser --disabled-password --gecos '' egg

#securityRestrictions
RUN chown -R root:egg /home/egg/
RUN chmod 750 /home/egg
RUN export TERM=xterm

WORKDIR /home/egg/

RUN pip install pycryptodome

COPY egg.py /home/egg
RUN chmod +x /home/egg/egg.py

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
