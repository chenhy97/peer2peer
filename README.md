# Comupter Network Project
Client & Server \\ Peer To Peer
-----------
## Important Points
### Peer 2 Peer 功能介绍：
- Client 可以有三个指令选择：GET、Upload、Quit
	>	Get:将Get报文发完总服务器之后可以获取Get数据源，然后再与		数据源建立连接。
	
	>	Upload:发送Upload报文，告诉服务器自己想要上传的文件，然后服务器将该文件名以及该客户机的IP、port加入文件项表中。
	
	>	Quit:断开与总服务器的连接，并同时关闭数据流。
	
- Server_Center 作为一个总枢纽，负责客户端发来的命令报文解析。然后根据命令分析的结果做出相应的工作
	>	由于需要处理多个客户机的请求，所以需要使用多线程
	
	>	_**难点**_：
	
		>	处理文件存储项表，删加操作(update_json)；
		>	多线程编写服务器规则(Handler)。
- p2p_ServerA 作为上传数据的peer。
	>  一个peer应该同时具有client和server俩个功能，当需要上传文件时打开server，当需要下载时打开client

	