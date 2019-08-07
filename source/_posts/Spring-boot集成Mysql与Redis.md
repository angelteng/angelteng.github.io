---
title: Spring boot集成Mysql与Redis
date: 2019-08-02 14:01:09
tags:
- Spring
- JAVA
categories: JAVA
---
# Mysql
pom.xml添加依赖
```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
    </dependency>
```
application.properties 添加mysql连接配置
```
    # Mysql配置
    spring.jpa.hibernate.ddl-auto=update
    spring.datasource.url=jdbc:mysql://localhost:3306/dbname
    spring.datasource.username=username
    spring.datasource.password=pwd
```
添加一个model
```java
    import javax.persistence.Entity;
    import javax.persistence.GeneratedValue;
    import javax.persistence.GenerationType;
    import javax.persistence.Id;

    @Entity // This tells Hibernate to make a table out of this class
    public class Users {
        @Id
        @GeneratedValue(strategy=GenerationType.AUTO)
        private Integer id;
        private String username;
        private String password;

        public Integer getId() {
            return id;
        }

        public void setId(Integer id) {
            this.id = id;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String name) {
            this.username = name;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String pwd) {
            this.password = pwd;
        }

    }
```
使用Spring boot JPA，集成CRUD接口
```java
    import com.example.demo.model.Users;
    import org.springframework.data.repository.CrudRepository;
    import java.util.*;

    // This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
    // CRUD refers Create, Read, Update, Delete

    public interface UsersRepository extends CrudRepository<Users, Integer> {

        List<Users> findByUsername(String username);

    }
```
在controller中使用
```java
    @RequestMapping("/find-by-username/{username}")
    public List findByUsername(@PathVariable("username") String username) {
        List<Users> userList = usersRepository.findByUsername(username);
        return userList;
    }
```

# Redis
pom.xml中添加依赖
```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>
```
application.properties中添加Redis连接配置
```
    # Redis数据库索引（默认为0）
    spring.redis.database=0
    # Redis服务器地址
    spring.redis.host=192.168.33.10
    # Redis服务器连接端口
    spring.redis.port=6379
    # Redis服务器连接密码（默认为空）
    spring.redis.password=
    # 连接池最大连接数（使用负值表示没有限制）
    spring.redis.jedis.pool.max-active=8
    # 连接池最大阻塞等待时间（使用负值表示没有限制）
    spring.redis.jedis.pool.max-wait=-1
    # 连接池中的最大空闲连接
    spring.redis.jedis.pool.max-idle=8
    # 连接池中的最小空闲连接
    spring.redis.jedis.pool.min-idle=0
    # 连接超时时间（毫秒）
    spring.redis.timeout=3000
```
controller中使用
```java
    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @RequestMapping("/setredis")
    public String setRedis(){
        redisTemplate.opsForValue().set("javaset","1");
        String ans = redisTemplate.opsForValue().get("javaset");
        return ans;
    }
```