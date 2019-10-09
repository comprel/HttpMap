
# HttpNetMap

介绍
```
HTTP 网络调用关系地图
依据主机上报http访问记录，构建调用关系，展示HTTP数据请求流向
```

部署：
部署准备：
. mysql
. neo4j
. kafka
. mongodb
. redis
python3环境

1. 获取源代码
略

2.新建目录
```
mkdir -p /usr/local/netmapService/service/
mkdir -p /usr/local/netmapService/run/
将源码放入/usr/local/netmapService/ 解压
```

3.初始化环境
```
cd /usr/local/netmapService/

pip install -r requirement.txt

```

4. 注册systemd服务：

```
cp etc/netmap-api.service /usr/lib/systemd/system
cp etc/netmap-tasks.service /usr/lib/systemd/system

chmod +x /usr/lib/systemd/system/netmap-api.service
chmod +x /usr/lib/systemd/system/netmap-tasks.service

systemctl daemon-reload
systemctl enable netmap-api.service
systemctl enable netmap-tasks.service

```

5. 修改配置：
```
修改 conf/app.conf 配置
```
6. 启动服务：

```
systemctl start netmap-client.service
systemctl enable netmap-client.service
```

备注：
若任务tasks处理能力不够， 可在一个host上启动多个netmap-tasks服务(注册多个服务即可)


