# Shinken Kafka logs storage

Simple Shinken broker module used to send logs into a Kafka Broker.

## Requirements
Use kafka-python > 1.3.0
```
   pip install kafka-python


## Enabling kafka module

To use the kafka-broker module you must declare it in your broker configuration.
```
   define broker {
      ...

      modules    	 ..., kafka-broker

   }
```

The module configuration is defined in the file: `kafka-broker.cfg`.

Default configuration needs to be tuned up to your Kafka Broker configuration.

# Configuration of Kafka module broker
define module{
     module_name         kafka-broker
     module_type         kafka-broker
     #bootstrap_servers – ‘host[:port]’ string (or list of ‘host[:port]’ strings) that the producer should contact to bootstrap initial cluster metadata. This does not have to be the full node list. It just needs to have at least one broker that will respond to a Metadata API Request. Default port is 9092. If no servers are specified, will default to localhost:9092.
     bootstrap_servers   localhost:9092

     #topic : topic where the message will be published. Default: Shinken
     topic               shinken

}
