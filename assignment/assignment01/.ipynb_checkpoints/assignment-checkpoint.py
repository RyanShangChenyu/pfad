import requests
from lxml import html
import datetime
import matplotlib.pyplot as plt
from scraping_utils import get_url, parse  #同文件夹的自义定函数文件，引用的时候不需要路径 只需要文件名
#get_url 自定义函数负责从网上down下数据   parse 负责解析网站文件的自定义函数
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

year = int(2024)
#命名一个文件名
filename = "crawled-page-run1.html".format(year=year)

# get page 下数据到文件
page = get_url('https://www.hko.gov.hk/tide/CCHtextPH2024.htm', filename)

# parse the page to html 解析html
tree = parse(page, 'html')

data = []

# initialize row counter  提取日期格式的相关数据的html表格
row_num = 0
# HTML格式的行的寻找
rows = tree.xpath("//html/body/table/tbody/tr")
print(f"找到的行数: {len(rows)}")  # 打印找到的行数
rows
#把行的数据遍历
for row in tree.xpath("//html/body/table/tbody/tr"
):
    columns = row.xpath("td")
    columns = [column.text_content() for column in columns]
    columns = [column.strip() for column in columns]
    row_string = " ".join(columns).strip()
    

    # skip empty rows 跳过空行
    if row_string.strip() == "":
        continue

    row_num += 1

    # print(f'Row {row_num}: {row_string}')
    #月份第一列 日期第二列 ---和老师不一样
    year=int(2024)
#月份是第一列
    month = int(columns[0])
    #日期是第二列
    day = int(columns[1])
 
    #第二个参数从len(colums)调整为我的确定数字就好

    for i in range(2,26, 2):
        # if columns[i] != "": #第二列会不执行这一步 去除这一列debug看看
            # get the time in HHMM format
            # hour = columns[i][:2] 我是固定列
              # 从 columns[i] 中提取小时和分钟
            hour = i-2  # 获取小时
            if hour>=23:
                hour=23
            # minute = 0  # 获取分钟 我这里不需要 可以不加

            dt = datetime.datetime(year,month,day,int(hour))
            value = columns[i+1] #第二列空 第三列2.15 第四列1.98  SO 避免第二列 ..
            # print(f'{dt} - {value}')
        #时间 和值组合在一起成为一个元组
            data.append((dt, value))    


# values取data的第二列
values = [item[1] for item in data]

# Convert to numpy array and float
values = np.array(values).astype(float)

# Calculate max and min values
max_value = np.max(values)
min_value = np.min(values)

# Normalize the values
norm = plt.Normalize(min_value, max_value)

# Create a colormap
cmap = plt.get_cmap('RdYlBu_r')

# Prepare the figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Scatter plot with normalized colors
sc = ax.scatter([record[0] for record in data], 
                 [float(record[1]) for record in data], 
                 c=norm(values),
                 alpha=1,
                 cmap=cmap,s=0.9)

# Add a colorbar
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Values')


cbar.locator = FixedLocator([0, 1])  # 设置刻度位置，这里以0和1为例
cbar.formatter = FixedFormatter([min_value, max_value])  # 设置刻度标签

ax.axhline(y=1, color='red', linestyle='--', label='y = 25',linewidth=1, alpha=0.5)  # 红色虚线
ax.axhline(y=2, color='blue', linestyle='--', label='y = 25',linewidth=1, alpha=0.5)
# ax.plot()
#用ax添加额外图
ax.plot([record[0] for record in data], [float(record[1]) for record in data],alpha=0.05)

# Show the plot
plt.show()