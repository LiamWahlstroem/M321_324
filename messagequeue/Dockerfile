FROM rabbitmq:3.11-management

WORKDIR /etc/rabbitmq
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672

CMD ["rabbitmq-server"]