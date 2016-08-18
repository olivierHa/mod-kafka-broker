#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2014:
#    Olivier Hanesse, olivier.hanesse@gmail.com
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

# This module send events to a Kafka Broker

from shinken.basemodule import BaseModule
from shinken.log import logger
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

properties = {
    'daemons': ['broker'],
    'type': 'kafka_broker',
    'external': False,
    }


# called by the plugin manager to get a broker
def get_instance(mod_conf):
    logger.info("[Kafka Broker] Get a Kafka broker module for plugin %s", mod_conf.get_name())
    instance = Kafka_broker(mod_conf)
    return instance


class Kafka_broker(BaseModule):

    def __init__(self, mod_conf):
        BaseModule.__init__(self, mod_conf)

        self.bootstrap_servers = getattr(mod_conf, 'bootstrap_servers', 'localhost:9092')
        self.topic = getattr(mod_conf, 'topic', 'shinken')
        self.producer = None

    def init(self):
        logger.info("[Kafka Broker] Initialization of the Kafka broker module")
        self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), 
                                      client_id='Shinken Broker module',
                                      acks=1,
                                      security_protocol='PLAINTEXT', # TODO: Support others
                                      bootstrap_servers=[self.bootstrap_servers])
        self.producer.send(self.topic,'[Kafka Broker] Init Shinken module Kafka')

    def close(self):
        self.producer.flush(10)
        self.producer.close(10)
        logger.debug('[Kafka Broker] Connection Closed')


    def manage_log_brok(self, brok):
        data = brok.data
        logger.debug("[Kafka Broker] Manage log brok %s", data)
        #The send() method is asynchronous. When called it adds the record to a buffer of pending record sends and immediately returns. This allows the producer to batch together individual records for efficiency.
        try:
          self.producer.send(self.topic, data['log'])
        except KafkaError as e:
          logger.debug('[Kafka Broker] Error sending logs to Kafka')
      
    def manage_brok(self, brok):
        """
        Overloaded parent class manage_brok method:
        - select which broks management functions are to be called
        """
        manage = getattr(self, 'manage_' + brok.type + '_brok', None)
        if manage:
            return manage(brok)
