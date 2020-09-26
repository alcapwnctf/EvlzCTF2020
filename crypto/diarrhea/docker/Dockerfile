FROM python:3-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd

#add user
RUN adduser --disabled-password --gecos '' diarrhea

#securityRestrictions
RUN chown -R root:diarrhea /home/diarrhea/
RUN chmod 750 /home/diarrhea
RUN export TERM=xterm

WORKDIR /home/diarrhea/

RUN pip install pycryptodome

COPY diarrhea.py /home/diarrhea
RUN chmod +x /home/diarrhea/diarrhea.py

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
