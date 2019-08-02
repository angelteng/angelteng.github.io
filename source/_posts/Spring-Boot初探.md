---
title: Spring Boot初探
date: 2019-07-30 15:54:58
tags:
- Java
- Spring
---
# 概念
1. Spring是一个生态体系（也可以说是技术体系），是集大成者，它包含了Spring Framework、Spring Boot、Spring Cloud等（还包括Spring Cloud data flow、spring data、spring integration、spring batch、spring security、spring hateoas）。
2. Spring Framework是整个Spring生态的基石。Spring官方对Spring Framework简短描述：为依赖注入、事务管理、WEB应用、数据访问等提供了核心的支持。
3. SpringMVC是基于Spring的一个MVC框架，用以替代初期的SSH框架。 Spring Framework本身没有Web功能，Spring MVC使用了WebApplicationContext类扩展ApplicationContext，使得拥有Web功能。
4. Spring Boot是基于Spring全家桶的一套快速开发整合包。以前的Java Web开发模式：Tomcat + WAR包。WEB项目基于Spring framework，项目目录一定要是标准的WEB-INF + classes + lib，而且大量的xml配置。Spring Boot为快速启动且最小化配置的spring应用而设计，并且它具有用于构建生产级别应用的一套固化的视图（约定）。
5. Spring Cloud事实上是一整套基于Spring Boot的微服务解决方案。它为开发者提供了很多工具，用于快速构建分布式系统的一些通用模式，例如：配置管理、注册中心、服务发现、限流、网关、链路追踪等。

# 跟着文档开始
基于Maven进行依赖包管理
1. 创建一个pom.xml，用于管理项目的依赖
spring-boot-starter-parent是一个特殊的启动器，提供有用的Maven默认值。
使用 mvn dependency:tree 可以打印项目的依赖项树形结构
```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>com.example</groupId>
        <artifactId>myproject</artifactId>
        <version>0.0.1-SNAPSHOT</version>

        <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>2.1.1.RELEASE</version>
        </parent>
        // 配置依赖性   
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
        </dependencies>
        // 打包配置
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>
    </project>
```
2. 来一个Hello World
```java
    import org.springframework.boot.*;
    import org.springframework.boot.autoconfigure.*;
    import org.springframework.web.bind.annotation.*;

    @RestController
    @EnableAutoConfiguration
    public class Example {

        @RequestMapping("/")
        String home() {
            return "Hello World!";
        }

        public static void main(String[] args) throws Exception {
            SpringApplication.run(Example.class, args);
        }
    }
```
- @RestController 是一个构造性注释，代表这是一个Controller类
- @RequestMapping 是一个路由注释
- 上面这两个注释都是基于Spring MVC
- @EnableAutoConfiguration 注释告诉Spring Boot根据你添加的jar依赖关系“猜测”你想要如何配置Spring。由于spring-boot-starter-web添加了Tomcat和Spring MVC，因此自动配置假定您正在开发Web应用程序并相应地设置Spring。
3. 运行
利用IDE 的 “RUN”， 活着 mvn spring-boot:run，可以看到启动了嵌入了Tomcat服务器在8080端口。
4. 打包
在pom.xml配置了build配置项后，运行mvn package会在target目录打包出一个可执行文件myproject-0.0.1-SNAPSHOT.jar跟一个myproject-0.0.1-SNAPSHOT.jar.original小文件。通过以下命令可以直接运行这个jar包。
```
    java -jar target/myproject-0.0.1-SNAPSHOT.jar
```
# Spring Boot的使用
1. Starters是一组方便的依赖描述符，您可以在应用程序中包含这些描述符。您可以获得所需的所有Spring和相关技术的一站式服务。通常以 spring-boot-starter-* 命名。Starters列表可以参考文档。
2. 构建代码
    - package命名
    - @SpringBootApplication 放在主类

3. 使用@SpringBootApplication Annotation
    - @EnableAutoConfiguration：启用Spring Boot的自动配置机制
    - @ComponentScan：对应用程序所在的软件包启用@Component扫描
    - @Configuration：允许在上下文中注册额外的beans或导入其他配置类
4. @SpringBootApplication注释等效于使用@Configuration、@EnableAutoConfiguration、@ComponentScan及其默认属性。

参考：
[Spring Boot 中文文档](https://springcloud.cc/spring-boot.html#using-boot-structuring-your-code)
[面试官问我：spring、springboot、springcloud的区别，我笑了](https://blog.csdn.net/weixin_44175121/article/details/90297426)