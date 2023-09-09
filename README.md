# konachan_spider
A spider to crawl images from konachan. Thanks to konachan for providing such convenient APIs !!!

> 开源项目链接：https://github.com/MYJOKERML/konachan_spider

一张张地点图片链接+看图片的方式实在是效率太低也太麻烦，碰巧最近在学习训练生成式AI，想找点自己的数据集，就想着爬点图片的说，然后konachan真的是神啊！！！，不仅提供好多好看的图片（嘿嘿嘿），还有非常完整的[API调用文档](https://konachan.net/help/api)，简直就是用来练习爬虫的第一神器，又有动力又易于学习。

好，话不多说，直接上代码，代码已开源，项目地址：https://github.com/MYJOKERML/konachan_spider

## 如何运行

```bash
git clone https://github.com/MYJOKERML/konachan_spider
cd konachan_spider
pip install -r requirements.txt
```

到此已经安装完所有依赖，其实就俩：`request` 用来发送请求，`fake_useragent` 用来随机生成一个user-agent。

接着你可以调整些代码的一些变量和细节以便更好地爬到你喜欢的图片。

1. `safe_mode`: 默认开启，konachan有一些好看的东西，懂的都懂，就不说了，越说感觉自己越像个死肥宅。。。
2. `proxies_on`: 是否开启代理，默认不开代理，这样会很慢，也有可能失败，失败后会自动尝试重连，如果一直连接失败的话请尝试开启代理。**开启代理请修改 `proxiex` 为自己代理端口**，否则会出现连接不上的情况。
3. `save_path`：图片储存路径。Windows默认 `f"D:\\dataset\\konachan\\{date}\\"+tag`，Linux默认`f'./dataset/konachan/{date}/'+tag` 
4. `tag`：你想要爬取图片的标签，可以上[网页版](https://konachan.net/post)看看自己的标签到底搜不搜得到图片再爬取，要准确知道标签信息，否则经常会搜不出图片
5. `pages_num`: 默认爬取几页，一页有21张图片

改完了之后就可以运行代码了,

**异步爬取，速度块**：

如果不在乎流量的话，强烈建议使用异步爬虫进行爬取，爬取速度是顺序执行的10几倍。

```bash
python spider_async.py
```

**依次爬取，效率较低**

运行 "konachan.py"：

```bash
python konachan.py
```

接着等数据（老婆）下载就行啦

## Upate 2023-9-9

更新了异步爬取图片的程序 "spider_async.py"，调整参数的方法同上。

默认代理关闭，端口改为了7890，为clash的默认端口。



