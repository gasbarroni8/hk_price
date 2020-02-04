### 香港代购价格爬虫
> 使用爬虫爬取香港大商场的实时价格，便于代购们的快速比价
#### requirements
* python3
* scrapy
#### 支持商场
1. [dfs](https://www.dfsglobal.cn/cn/hong-kong)
2. [sasa](https://hongkong.sasa.com/SasaWeb/tch/sasa/home.jsp)

#### 使用
```sh
# 下载
git clone git@github.com:Moersity/hk_price.git
cd hk_price

# 安装scrapy
pip install scrapy

# 获取sasa价格, 以csv格式保存
scrapy crawl sasa -o sasa.csv

# 获取dfs价格，以json保存
scrapy crawl dfs -o dfs.json
```

#### 输出
![Example](./example.png)

