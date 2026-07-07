---
Authors: Django Wong
Date: 2015-10-20
Summary: Kafka提供了类似于JMS的特性，但是在设计实现上完全不同，此外它并不是JMS规范的实现。kafka对消息保存时根据Topic进行归类，发送消息者成为Producer,消息接受者成为Consumer,此外kafka集群有多个kafka实例组成，每个实例(server)成为broker。。
Title: Kafka基本操作
seo_description: 学习Kafka基本操作，包括启动Kafka、创建Topic、发送和接收消息的详细步骤。本文还提供了Python脚本示例，帮助您快速掌握Kafka消息队列的核心功能，适合初学者和开发者参考。
seo_keywords: Kafka基本操作, Kafka启动, 创建Topic, Kafka生产者, Kafka消费者
---

## 启动Kafka

```bash
bin/kafka-server-start.sh config/server.properties&
```

##　创建一个Topic

```bash
bin/kafka-topics.sh --create --topic test1 --partitions 1  --replication-factor 1 --zookeeper 127.0.0.1:2181
```

然后查看一下

```bash
bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

## 创建发送者

```bash
bin/kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic test1
```

## 创建消费者

```bash
bin/kafka-console-consumer.sh --zookeeper 127.0.0.1:2181 --from-beginning --topic test1
```

## 写一个简单的python脚本

```bash
#/usr/bin/python
#coding=utf-8

from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")

topics = client.topics
topic = topics['test1']
producer = topic.get_producer()
producer.produce('test message 45')

print "==================="
consumer = topic.get_simple_consumer()
for message in consumer:
	if message is not None:
		print message.offset, message.value
```