---
title: Spring boot 集成Kafka
date: 2019-08-05 22:27:03
tags:
- Spring boot
- JAVA
categories: JAVA
---
1. pom.xml添加依赖
```xml
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
        <version>2.2.7.RELEASE</version>
    </dependency>
```
2. application.properties添加配置
```
    #============== kafka ===================
    # 指定kafka 代理地址，可以多个
    spring.kafka.bootstrap-servers=127.0.0.1:9092

    #=============== provider  =======================

    spring.kafka.producer.retries=0
    # 每次批量发送消息的数量
    spring.kafka.producer.batch-size=16384
    spring.kafka.producer.buffer-memory=33554432

    # 指定消息key和消息体的编解码方式
    spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
    spring.kafka.producer.value-serializer=org.apache.kafka.common.serialization.StringSerializer

    #=============== consumer  =======================
    # 指定默认消费者group id
    spring.kafka.consumer.group-id=test-consumer-group
    #
    spring.kafka.consumer.auto-offset-reset=earliest
    spring.kafka.consumer.enable-auto-commit=true
    spring.kafka.consumer.auto-commit-interval=100

    # 指定消息key和消息体的编解码方式
    spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
    spring.kafka.consumer.value-deserializer=org.apache.kafka.common.serialization.StringDeserializer

```
3. 生产者 
```java
    import com.google.gson.Gson;
    import com.google.gson.GsonBuilder;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.context.annotation.Configuration;
    import org.springframework.kafka.core.KafkaTemplate;
    import java.util.*;

    @Configuration
    public class MessageSender {

        @Autowired
        private KafkaTemplate<String,String> kafkaTemplate;

        private Gson gson = new GsonBuilder().create();

        public void send(String msg){
            Message message = new Message();
            message.setId(System.currentTimeMillis());
            message.setMsg(msg);
            message.setTime(new Date());
            kafkaTemplate.send("test_topic", gson.toJson(message));
        }
    }
```
Message类
```java
    import java.util.*;
    public class Message {
        private Long id;
        private String msg;
        private Date time;

        public void setId(Long id) {
            this.id = id;
        }
        public void setMsg(String msg){
            this.msg = msg;
        }
        public  void setTime(Date time){
            this.time = time;
        }
    }
```

4. 消费者
```java
    import org.apache.kafka.clients.consumer.ConsumerRecord;
    import org.springframework.context.annotation.Configuration;
    import org.springframework.kafka.annotation.KafkaListener;

    import java.util.Optional;

    @Configuration
    public class MessageReceiver {

        @KafkaListener(topics = {"test_tipic"})
        public void listen(ConsumerRecord<?, ?> record) {

            Optional<?> kafkaMessage = Optional.ofNullable(record.value());

            if (kafkaMessage.isPresent()) {

                Object message = kafkaMessage.get();
                System.out.println(message);
            }

        }
    }
```


参考：
[Spring Boot系列文章（一）：SpringBoot Kafka 整合使用](http://www.54tianzhisheng.cn/2018/01/05/SpringBoot-Kafka/)