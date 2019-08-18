---
title: 《Head first Servlet & JSP》笔记
date: 2019-07-02 14:10:15
tags:
- JAVA
categories: JAVA 
---
# Web应用体系结构
1. Servlet 生命周期：
    1. servlet类加载
    2. servlet实例化
    3. 调用init方法
    4. 调用service方法
    5. 调用destory方法

2. Servlet没有main方法，他们受控于另一个JAVA容器应用，如Tomcat。
    Web服务器应用（ng、Apache）-> Web容器应用(Tomcat) -> Servlet

3. 容器的作用：
    1. 通信支持：管理与web服务器的通信。
    2. 生命周期管理：控制Servlet的生命周期、垃圾回收。
    3. 多线程支持：管理一个线程池，为每个Servlet请求创建一个新/分配的Java线程。
    4. 声明方式实现安全：XML描述文件。
    5. JSP支持：将JSP翻译成JAVA。
4. MVC
{% asset_img 0.png mvc %}
5. J2EE 包含了Servlet规范、JSP规范、EJB规范，Web容器用于Web组件（Servlet、JSP），EJB容器用于业务组件。
    - 独立的Web容器：Tomcat、Resin
    - J2EE服务器：WebLogic、WebSphere

# Servlet
1. 容器调用流程
    - 容器 --> servlet.init() 
    - 容器的线程 --> service() --> doGet()/doPost()...
2. service方法总是在自己的栈中调用

# Request and Response
1. ServletRequest
    - getAttribute(String)
    - genContentLength()
    - getInputStream() 输入流
    - getLocalPort()  请求最后发送到到端口（每个线程有不同到本地端口）
    - getRemotePort() 客户端的端口
    - getServerPort() 请求原来发送到的端口
    - getParameter(String)
    - getParameterValues(String)
    - getParameterName
2. HttpServletRequest extends ServletRequest
    - getContextPath()
    - getCookies()
    - getHeader()
    - getMethod()
    - getQueryString()
    - getSession()

3. ServletResponse
    - getBufferSize()
    - setContentType()
    - getOutputStream(): 输出字节 ServletOutputStream s = response.getOutputStream(); out.write(Byte);
    - getWriter(): 输出字符 PrintWriter w = response.getWriter(); w.println(String);
    - setContentLength()

3. HttpServletResponse extends ServletResponse
    - addCookie()
    - addHeader()
    - encodeURL()
    - sendError()
    - setStatus()
    - setRedirect()
    
4. HttpServletResponse常用setContentType()和getWrite()/getOutputStream()

# 初始化
1. getServletContext().getInitParameter("email") ,对应用中所有的servlet跟jsp都可用 ,非线程安全。
   ```xml
    <web-app>
        <context-param>
            <param-name>email</param-name>
            <param-value>sdfsd</param-value>
        </context-param>
    </web_app>
   ```
2. getServletConfig().getInitParamter("email")，只对该servlet可用
   ```xml
    <web-app>
        <servlet>
            <init-param>
                <param-name>email</param-name>
                <param-value>sdfsd</param-value>
            </init-param>
        </servlet>
    </web_app>
   ```
3. 监听Webapp，ServletContextListener