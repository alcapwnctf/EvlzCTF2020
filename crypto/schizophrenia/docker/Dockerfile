FROM python:3-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd

#add user
RUN adduser --disabled-password --gecos '' schizophrenia

#securityRestrictions
RUN chown -R root:schizophrenia /home/schizophrenia/
RUN chmod 750 /home/schizophrenia
RUN export TERM=xterm

WORKDIR /home/schizophrenia/

RUN pip install pycryptodome

COPY schizophrenia.py /home/schizophrenia
RUN chmod +x /home/schizophrenia/schizophrenia.py

ADD xinetd.conf /etc/xinetd.conf
CMD /etc/init.d/xinetd start; sleep infinity
EXPOSE 1337
