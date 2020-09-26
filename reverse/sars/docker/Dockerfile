FROM busybox:glibc
COPY server /
RUN chmod +x /server
WORKDIR /
CMD /server
EXPOSE 1337