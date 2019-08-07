---
title: Spring boot集成Websocket
date: 2019-08-07 11:36:19
tags:
- Spring
- JAVA
categories: JAVA
---
1. pom.xml配置依赖
```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-websocket</artifactId>
    </dependency>
```
2. 添加Websocket配置类
```java
    import org.springframework.context.annotation.Configuration;
    import org.springframework.messaging.simp.config.MessageBrokerRegistry;
    import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
    import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
    import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

    @Configuration
    @EnableWebSocketMessageBroker
    public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

        @Override
        public void configureMessageBroker(MessageBrokerRegistry config) {
            /**
            * 配置消息代理
            * 启动简单Broker，消息的发送的地址符合配置的前缀来的消息才发送到这个broker
            */
            config.enableSimpleBroker("/topic");
            config.setApplicationDestinationPrefixes("/app");
        }

        @Override
        public void registerStompEndpoints(StompEndpointRegistry registry) {
            /**
            * 注册 Stomp的端点
            * addEndpoint：添加STOMP协议的端点。这个HTTP URL是供WebSocket或SockJS客户端访问的地址
            * withSockJS：指定端点使用SockJS协议
            */
            registry.addEndpoint("/websocket-demo")
                    .setAllowedOrigins("*")
                    .withSockJS();
        }

    }
```
3. 添加Controller
```java
    import com.example.demo.service.RequestMessage;
    import com.example.demo.service.ResponseMessage;
    import org.springframework.messaging.handler.annotation.MessageMapping;
    import org.springframework.messaging.handler.annotation.SendTo;
    import org.springframework.stereotype.Controller;
    import java.util.concurrent.atomic.AtomicInteger;

    @Controller
    public class BroadcastController {
        // 收到消息记数
        private AtomicInteger count = new AtomicInteger(0);

        /**
        * @MessageMapping 指定要接收消息的地址，类似@RequestMapping。除了注解到方法上，也可以注解到类上
        * @SendTo默认 消息将被发送到与传入消息相同的目的地
        * 消息的返回值是通过{@link org.springframework.messaging.converter.MessageConverter}进行转换
        * @param requestMessage
        * @return
        */
        @MessageMapping("/receive")
        @SendTo("/topic/getResponse")
        public ResponseMessage broadcast(RequestMessage requestMessage){
            ResponseMessage responseMessage = new ResponseMessage();
            try {
                Thread.sleep(1000);
            }
            catch(InterruptedException e) {
                System.out.println("got interrupted!");
            }
            responseMessage.setResponseMessage("Server receive [" + count.incrementAndGet() + "] records");
            return responseMessage;
        }
    }
```
4. 前端
```javascript
    <!-- jquery  -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js"></script>
    <!-- stomp协议的客户端脚本 -->
    <script src="http://cdn.bootcss.com/stomp.js/2.3.3/stomp.min.js"></script>
    <!-- SockJS的客户端脚本 -->
    <script src="http://cdn.jsdelivr.net/sockjs/1.0.1/sockjs.min.js"></script>
    <script type="text/javascript">
        var stompClient = null;

        function connect() {
            // websocket的连接地址，此值等于WebSocketMessageBrokerConfigurer中registry.addEndpoint("/websocket-simple").withSockJS()配置的地址
            var socket = new SockJS('http://127.0.0.1:8080/websocket-demo');
            stompClient = Stomp.over(socket);
            stompClient.connect({}, function(frame) {
                setConnected(true);
                console.log('Connected: ' + frame);

                // 客户端订阅消息的目的地址：此值BroadcastCtl中被@SendTo("/topic/getResponse")注解的里配置的值
                stompClient.subscribe('/topic/getResponse', function(respnose){
                    showResponse(JSON.parse(respnose.body).responseMessage);
                });
            });
        }

        function disconnect() {
            if (stompClient != null) {
                stompClient.disconnect();
            }
            setConnected(false);
            console.log("Disconnected");
        }

        function sendName() {
            var name = $('#name').val();
            // 客户端消息发送的目的：服务端使用BroadcastCtl中@MessageMapping("/receive")注解的方法来处理发送过来的消息
            stompClient.send("/app/receive", {}, JSON.stringify({ 'name': name }));
        }

        function showResponse(message) {
            var response = $("#response");
            response.html(message + "\r\n" + response.html());
        }
    </script>
```

参考：
[Using WebSocket to build an interactive web application](https://spring.io/guides/gs/messaging-stomp-websocket/)