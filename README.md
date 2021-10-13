# 美多商城 — Django 开发

## 前言

> 本项目属于网上自学项目，注重熟悉业务功能开发以及扩展技术知识面。了解前沿的技术解决方案。并新增了一些自己的设计，例如：统一异常处理，状态码枚举类、项目 `html` 网页模板路径汇总类，以及 `Cookie, Redis` 键名的设计与封装等。尽量的让项目避免出现 **魔法值**，提高项目的可扩展性和可维护性。

<br/>

## 项目概述

美多商城属于 `B2C` 电商平台，商城销售自营商品给顾客。系统前台包括 **商品列表、商品详情、商品搜索、购物车、订单支付、评论、用户中心** 等核心业务功能，系统后台包括商品管理、运营管理、用户管理、系统设置等系统管理功能。

<br/>

## 项目技术栈

| 名称                  | 说明                     |
| --------------------- | ------------------------ |
| Django                | Django Web开发框架       |
| Django REST framework | Django REST规范的Web框架 |
| Vue                   | 前端 JavaScript 框架     |
| MySQL                 | MySQL 数据库             |
| Redis                 | Redis 缓存数据库         |
| Celery                | 分布式任务队列           |
| FastDFS               | 分布式文件存储系统       |
| ElasticSearch         | 全文检索框架             |
| alipay                | 阿里支付                 |
| OAuth 2.0             | 第三方授权认证           |
| docker                | 容器化引擎               |

<br/>

## 项目架构图

![美多项目架构.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bbe2fe3e0ff449df82fb3a7e1074dde0~tplv-k3u1fbpfcp-watermark.image?)

<br/>

## 初始开发环境

| 环境 / 工具 | 版本                | 说明              |
| ----------- | ------------------- | ----------------- |
| Python      | 3.7.9               | Python 解释器     |
| Django      | 3.2.7               | Django 框架       |
| Jinja2      | 2.10                | 模板引擎          |
| PyCharm     | Professional 2020.2 | Python IDE 编辑器 |
| MySQL       | 8.0.26              | MySQL 数据库      |

<br/>

上面就是项目的初始开发环境，项目后续所需的第三方库环境在 `meiduo_mall` 下的 `requirements.txt` 文件中。可以使用如下命令全部安装。

```python
pip install -r requirements.txt
```

<br/>

## 项目模块划分

### 系统前台

- 首页内容广告模块 - contents
- 用户模块 - users
- 校验模块 - verifications
- 认证模块 - oauth
- 省市区三级联动模块 - areas
- 商品模块 - goods
- 购物车模块 - carts
- 订单模块 - orders
- 支付模块 - payment

<br/>

### 系统后台

- 商品管理模块 - 
- 运营管理模块 - 
- 用户管理模块 - 
- 系统设置模块 - 

<br/>

## 项目特色

1. 自定义用户认证后端，实现多账户登录，基于 `OAuth2.0`，实现第三方登录。 
2. 采用 `Redis` 作为消息中间件，配合 `Celery` 完成异步发送邮件与短信验证码。 
3. 采用分布式文件系统 `FastDFS` 作为文件存储系统，存储项目静态图片。 
4. 采用 `Haystack+Elasticsearch` 实现商品的搜索。
5. 采用 `docker` 容器化技术搭建项目环境。 
6. 数据库事务 + 乐观锁解决并发订单保存问题。
7. 网站首页、商品详情页进行页面静态化，提升网站性能。
8. `MySQL` 主从同步，读写分离实现数据库负载均衡。

<br/>

## 项目页面展示/体验

- [系统前台体验](http://mp-meiduo-python.itheima.net/)，账号 `admin`，密码 `admin`
- [系统后台体验](http://mp-meiduo-python.itheima.net/static/dist/#/)，账号 `admin`，密码 `admin`

<br/>

### 广告首页

![首页01](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/324af37cd81444429dc77b530edb8437~tplv-k3u1fbpfcp-watermark.image?)

![1F手机通讯](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3da6901d28a9466fbea4afbb83233239~tplv-k3u1fbpfcp-watermark.image?)


![2F电脑数码](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/65be9037ddde4b0b9668a21e70f6c8a6~tplv-k3u1fbpfcp-watermark.image?)


![3F家居安装](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a9e80b465aa44276ae798188791ada0d~tplv-k3u1fbpfcp-watermark.image?)

<br/>

### 商品详情

![商品详情](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1e64a3b1e6264724961dcf4b4d20f3ce~tplv-k3u1fbpfcp-watermark.image?)

<br/>

### 购物车

![购物车](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3a493fde36e64b49ab5be6c99ef3d42f~tplv-k3u1fbpfcp-watermark.image?)

<br/>

## 项目资料

<br/>

## 项目部署

<br/>

## 尾语

**✍ 用  Code 谱写世界，让生活更有趣。❤️**

**✍ 万水千山总是情，点赞再走行不行。❤️**

**✍ 码字不易，还望各位大侠多多支持。❤️**