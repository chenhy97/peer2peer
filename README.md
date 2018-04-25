# Comupter Network Project
Client & Server \\ Peer To Peer
-----------
## Important Points
###		实验环境：
-	编程语言：python3
	为什么选择python呢，是因为python提供了很多很方便的库函数，包括threading，socket
server，socket，struct，os等。可以非常方便的搭建一个服务器。更为处理字符串提供了便利。
-	编译环境：pycharm
###	Peer 2 Peer 功能介绍：
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

###	 Client-Server 功能介绍：
- Client	同样是可以发送GET报文到服务器，然后从服务器获取文件。也可以发送quit指令来断开与服务器之间的连接。
- Server	可以处理俩种类型的指令报文，当收到Client报文时，会分析报文中包含的文件名。然后根据这个文件名查找服务器中相应的文件，如果有则打包发给客户端。如果没有则发送“Not Exist”报文。

###		Peer 2 Peer 流程说明
-	首先打开Server_Center，由他来作为中转枢纽，提供peers中有文件的peers的ip与端口
- 	打开俩个含有该文件的peers，由于它实现的功能类似于C/S模型中的服务器，所以我们将它称为p2p_ServerA与p2p_ServerB
-  再打开client客户端，client发送get报文之后，center告诉client哪个peers存在他所需要的文件，然后client就和这些peers建立数据连接，开始传输数据。
-  当数据传输完成之后，client可以发送quit指令报文给center，断开连接。
###		Peer 2 Peer 协议分析
-	具体过程在流程说明中已经说明。
- 	现在我们来分析一下命令报文的格式：
	>	ds