import pyaudio # 收集声音
import numpy as np # 处理声音数据
import matplotlib.pyplot as plt # 作图
import matplotlib as mpl
import matplotlib.colors as mcolors

# 按键中断: 按下按键执行该函数
def on_press(event):
    global stream, p, END
    if event.key == 'q':
        plt.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        END = True

# 输入音频参数设置
END = False
# CHUNK = 1024 * 8
CHUNK = 100 #看组织数量
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNEL, rate=RATE,\
    input=True, frames_per_buffer=CHUNK)

# 关闭工具栏
mpl.rcParams['toolbar'] = 'None'

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 3))#,subplot_kw={'projection': 'polar'} 改成极坐标
plt.subplots_adjust(left=0.001, top=0.999, right=0.999, bottom=0.001)
plt.get_current_fig_manager().set_window_title('Wave')

# 创建 x 轴数据
x = np.arange(0, CHUNK)

# 创建颜色映射
norm = mcolors.Normalize(0, 2**8)
cmap = plt.get_cmap('cool')  # 选择一个颜色映射

# 生成随机数据并绘制柱状图
data = np.random.rand(CHUNK) * (2**7)  # 生成随机数据并放大
bars = ax.bar(x, data, color=cmap(norm(data)))

# 设置坐标轴范围
ax.set_xlim(0, CHUNK - 1)
ax.set_ylim(0, 2**8)  # 修改为适合柱状图的范围
plt.axis('off')  # 关闭坐标轴

# 启用交互模式
plt.ion()
plt.show()

# 程序主体
while END==False:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(data, dtype=np.int16)
    #记得改成对应图名 bars lint plot 
    # bars.set_ydata(data)
    # 更新条形图的高度
    for bar, height in zip(bars, data):
        bar.set_height(height)
        # 根据高度设置颜色
        color = cmap(norm(height))
        bar.set_color(color)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.05)