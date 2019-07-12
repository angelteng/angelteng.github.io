---
title: OAuth2授权
date: 2019-07-09 14:06:19
tags: 
---
# OAuth是一个标准
开放授权（OAuth）是一个开放标准，允许用户让第三方应用访问该用户在某一网站上存储的私密的资源（如照片，视频，联系人列表），而无需将用户名和密码提供给第三方应用。
OAuth是OpenID的一个补充，但是完全不同的服务。

# OAuth功能
OAuth允许用户提供一个令牌，而不是用户名和密码来访问他们存放在特定服务提供者的数据。每一个令牌授权一个特定的网站（例如，视频编辑网站)在特定的时段（例如，接下来的2小时内）内访问特定的资源（例如仅仅是某一相册中的视频）。这样，OAuth让用户可以授权第三方网站访问他们存储在另外服务提供者的某些特定信息，而非所有内容。

# OAuth四种授权方式
1. Authorization Code
    {% asset_img 0.jpg %}
    - （A）Client使用浏览器（用户代理）访问Authorization server。也就是用浏览器访问一个URL，这个URL是Authorization server提供的，访问的收Client需要提供（客户端标识，请求范围，本地状态和重定向URL）这些参数。
    - （B）Authorization server验证Client在（A）中传递的参数信息，如果无误则提供一个页面供Resource owner登陆，登陆成功后选择Client可以访问Resource server的哪些资源以及读写权限。
    - （C）在（B）无误后返回一个授权码（Authorization Code）给Client。
    - （D）Client拿着（C）中获得的授权码（Authorization Code）和（客户端标识、重定向URL等信息）作为参数，请求Authorization server提供的获取访问令牌的URL。
    - （E）Authorization server返回访问令牌和可选的刷新令牌以及令牌有效时间等信息给Client。
    
    当采用jwt/传统cookie session登录模式下，可以有两种不同的流程，上面为传统登录模式，下面为jwt登录模式。
    {% asset_img 4.jpg%}

2. Implicit
    {% asset_img 1.jpg %}
    和Authorzation Code类型下重要的区分就是省略了Authorization Response和Access Token Request。
3. Resource Owner Password Credentials Grant
    {% asset_img 2.jpg %}
    Client直接使用Resource owner提供的username和password来直接请求access_token（直接发起Access Token Request然后返回Access Token Response信息）。这种模式一般适用于Resource server高度信任第三方Client的情况下。
4. Client Credentials Grant
    {% asset_img 3.jpg %}
    Client直接已自己的名义而不是Resource owner的名义去要求访问Resource server的一些受保护资源。

# 安全性问题
1. 要求Authorization server进行有效的Client验证； 
    包括client是否注册、client所属权限。
2. client_serect,access_token,refresh_token,code等敏感信息的安全存储（不得泄露给第三方）、传输通道的安全性（TSL的要求）；
    必须使用HTTPS。
3. 维持refresh_token和第三方应用的绑定，刷新失效机制；
4. 维持Authorization Code和第三方应用的绑定，这也是state参数为什么是推荐的一点，以防止CSRF；
    同3，要求验证请求来源域名、重定向域名是否合法。
    必须使用state：客户端发出去, 授权服务器原样返回(对于授权服务器来说state是黑盒的东西,说也是可有可无的存在)，所以这个参数如何运用，全靠客户端。比如如果“李四”在客户端已经登录，那么客户端在发送state的时候就可以把“李四”的标识信息和随机数等其他信息加密后作为state。同时存入自己的cookie中。在接收到回调后先对比验证cookie，然后从里面取出“李四”。



主要参考：
[[认证 & 授权] 1. OAuth2授权](https://www.cnblogs.com/linianhui/p/oauth2-authorization.html#auto_id_0)