# getIpDelayTime
1. 获取本地到其他地区的ip时延，主要是通过调用Excel表格获取数据和存储数据
2. 主要有是通过python中的xrld和xlwt库来对Excel进行操作。
3. 使用到了python中的多进程来获取时延，但是Windows下python中没有比较好的写文件锁，通过让每个进程来读取文件的不同部分来获取时延数据。
4. 后期再通过对Excel操作将多个文件合并成一个文件，间接的实现了多个文件写。
5. 最后将本程序打包成可以在Windows下可以直接运行的.exe文件，让不同地区的主机运行，即可获取到不同地区到不同地区的ip时延。