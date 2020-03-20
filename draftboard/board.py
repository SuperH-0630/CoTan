import time
import os
import logging

import pygame
from pygame.locals import *

from draftboard.toolbox import tool_box
from system import basicConfig, QueueController

queue_controller = QueueController()
logging.basicConfig(**basicConfig)

# 定义一些变量
pen_color = [0, 0, 0]  # 画笔颜色
increasing_color = [0, 0, 255]
subtraction_color = [255, 0, 0]
pen_weight = 2  # 圆形的粗细（线条*2）=中笔
previous_x = None
previous_y = None  # 为画图所准备的
continuous_draw = False  # 设置免按
coordinate_system_drawing_method = 0
coordinate_click_point = [0, 0, 0]  # 根据点击中键记录坐标系的点，没有记录则为数字0，记录则为数组
record_origin_x = 0
record_origin_y = 0  # 原点坐标
horizontal_pixels = []  # X点
ordinate_pixels = []  # Y点
horizontal_scale = []  # X个数
ordinate_scale = []  # Y个数
anchor_x = []
anchor_y = []
span = 60  # 坐标系跨度调节
middle_key = 0  # 中键模式
line = []  # 画线列表
rect = []  # 画矩阵和圆列表
poly = []  # 画多边形列表
tips = ''  # 设置备注
save_dir = ''  # 保存路径
bottom_tip = [0, 0, 0, 0, 0]  # 底部显示信息[x,y,左键，中间，右键]
mode = {1: '绘制坐标系', 2: '绘制直线(g)', 3: '填充矩形(f)', 4: '线条矩形(s)',
        5: '绘制横线(k)', 6: '绘制竖线(l)', 7: '绘制多段线(j)',
        8: '绘制横打点多段线(i)', 9: '绘制竖打点多段线(u)', 10: '坐标测绘(h)',
        11: '绘制虚线(q)', 12: '填充圆形(c)', 13: '线条圆形(v)', 14: '多边形(n-填充,m-线条)',
        15: '填充椭圆形(e)', 16: '线条椭圆形(r)', 0: 'None'}  # 快捷键名字
SCREEN_X = 900
SCREEN_Y = 700
init_done = None
FONT = None
SCREEN = None
SCREEN_CAPTION = None

def start_gui():
    global init_done, FONT, SCREEN, SCREEN_CAPTION
    init_done = pygame.init()  # 初始化所有模块
    FONT = pygame.font.Font(fr'Font{os.sep}ZKST.ttf', 16)  # 设置字体(Linux下应该用\而不是/)
    SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0)  # 创建屏幕
    SCREEN_CAPTION = pygame.display.set_caption('CoTan草稿板')  # 定义标题（后期加上定义Logo）
    SCREEN.fill([255, 255, 255])  # 默认用白色填充窗口
    pygame.display.set_icon(pygame.image.load(f'Pic{os.sep}favicon.ico'))


def func_draw(func_list, pixel_accuracy=1000):
    global horizontal_pixels, horizontal_scale, ordinate_pixels, ordinate_scale, anchor_y, anchor_x, pen_color
    global increasing_color, subtraction_color
    c = [0, 0, 0]  # 增函数颜色

    def x_convert_pixels(x_coordinate):
        return ((x_coordinate - horizontal_scale[0]) / (horizontal_scale[1] - horizontal_scale[0]) *
                (horizontal_pixels[1] - horizontal_pixels[0]) + horizontal_pixels[0])

    def y_convert_pixels(y_coordinate):
        return ((y_coordinate - ordinate_scale[0]) / (ordinate_scale[1] - ordinate_scale[0]) *
                (ordinate_pixels[1] - ordinate_pixels[0]) + ordinate_pixels[0])

    for i in func_list:
        last_x = None  # 上一组X和Y
        last_y = None
        if func_list is None:
            continue
        func = func_list[i]
        try:
            for x in range((horizontal_scale[0] - 1) * pixel_accuracy, (horizontal_scale[1] + 1) * pixel_accuracy, 1):
                x /= pixel_accuracy
                try:
                    y = func(x)
                except ValueError:
                    last_x = None
                    last_y = None
                    continue
                try:
                    now_x = x_convert_pixels(x)
                    now_y = y_convert_pixels(y)
                    if now_y > anchor_y[0] or now_y < anchor_y[1] or now_x < anchor_x[0] or now_x > anchor_x[1]:
                        last_x = None
                        last_y = None
                        continue
                except TypeError:  # 预防复数
                    continue
                if last_x is not None:
                    if last_y > now_y:
                        c = increasing_color  # 增函数
                    elif last_y < now_y:
                        c = subtraction_color  # 减函数#改为检查Y数值而不是坐标
                    pygame.draw.line(
                        SCREEN, c, (int(last_x), int(last_y)), (int(now_x), int(now_y)), pen_weight)
                last_x = now_x
                last_y = now_y
        except IndexError:
            break


def draw_line(xy_coordinates: (list, tuple), with_point=False):
    global previous_x, previous_y
    if with_point:
        pygame.draw.circle(SCREEN, pen_color, xy_coordinates, pen_weight, 0)
    if previous_x is not None:
        pygame.draw.line(SCREEN, pen_color, (previous_x, previous_y), xy_coordinates, pen_weight)
    previous_x = xy_coordinates[0]
    previous_y = xy_coordinates[1]


def coordinate_draw(origin_x, origin_y, x_interval=(-100, 100),  # 三个点中，两边的两个点距离原点距离的一个list
                    y_interval=(-200, 100), scale_span=10, width=3, arrow=3, origin=3):
    scale_span = abs(scale_span)  # kd大于0
    global pen_weight, record_origin_x, record_origin_y, horizontal_scale, horizontal_pixels, ordinate_scale
    global ordinate_pixels, anchor_x, anchor_y
    record_origin_x = origin_x
    record_origin_y = origin_y  # 存储原点坐标
    anchor_x = [origin_x + x_interval[0], origin_x + x_interval[1]]  # 定位点
    anchor_y = [origin_y + y_interval[1], origin_y + y_interval[0]]
    pygame.draw.circle(SCREEN, pen_color, (origin_x, origin_y), origin, 0)  # 绘制原点
    pygame.draw.line(
        SCREEN, pen_color, (origin_x + x_interval[0], origin_y), (origin_x + x_interval[1], origin_y), pen_weight)
    pygame.draw.line(
        SCREEN, pen_color, (origin_x, origin_y + y_interval[0]), (origin_x, origin_y + y_interval[1]), pen_weight)
    negative_scale = 0  # 刻度统计
    negative_pixels = 0
    for i in range(origin_x, origin_x + x_interval[0], -scale_span):  # 右
        negative_scale -= 1
        pygame.draw.line(SCREEN, pen_color, (i, origin_y + width), (i, origin_y), pen_weight)
        negative_pixels = i
    positive_scale = 0
    positive_pixels = 0
    for i in range(origin_x, origin_x + x_interval[1], scale_span):  # 刻度#左
        positive_scale += 1
        pygame.draw.line(SCREEN, pen_color, (i, origin_y + width), (i, origin_y), pen_weight)
        positive_pixels = i
    horizontal_scale = [negative_scale + 1, positive_scale - 1]
    horizontal_pixels = [negative_pixels, positive_pixels]
    negative_scale = 0
    negative_pixels = 0
    for i in range(origin_y, origin_y + y_interval[0], -scale_span):  # 上
        negative_scale += 1
        pygame.draw.line(SCREEN, pen_color, (origin_x + width, i), (origin_x, i), pen_weight)
        negative_pixels = i
    positive_scale = 0
    positive_pixels = 0
    for i in range(origin_y, origin_y + y_interval[1], scale_span):  # 下
        positive_scale -= 1
        pygame.draw.line(SCREEN, pen_color, (origin_x + width, i), (origin_x, i), pen_weight)
        positive_pixels = i
    ordinate_scale = [positive_scale + 1, negative_scale - 1]
    ordinate_pixels = [positive_pixels, negative_pixels]

    # 箭头
    pygame.draw.line(
        SCREEN,
        pen_color,
        (origin_x + x_interval[1],
         origin_y),
        (origin_x + x_interval[1] - arrow,
         origin_y + arrow),
        pen_weight)  # X上
    pygame.draw.line(
        SCREEN,
        pen_color,
        (origin_x + x_interval[1],
         origin_y),
        (origin_x + x_interval[1] - arrow,
         origin_y - arrow),
        pen_weight)  # X下

    pygame.draw.line(
        SCREEN,
        pen_color,
        (origin_x,
         origin_y + y_interval[0]),
        (origin_x - arrow,
         origin_y + y_interval[0] + arrow),
        pen_weight)  # y左
    pygame.draw.line(
        SCREEN,
        pen_color,
        (origin_x,
         origin_y + y_interval[0]),
        (origin_x + arrow,
         origin_y + y_interval[0] + arrow),
        pen_weight)  # X下


def top_draw():
    # 绘制顶部
    global pen_weight, FONT, bottom_tip, SCREEN_X, SCREEN_Y, middle_key, save_dir, mode, continuous_draw, tips, line
    global record_origin_x, record_origin_y, rect, poly, pen_color, increasing_color, subtraction_color
    global coordinate_click_point, span
    if continuous_draw:
        key_d = '启动无点击画线(点击d关闭)'
    else:
        key_d = '关闭无点击画线'
    pygame.draw.rect(SCREEN, [255, 255, 255], [0, 0, SCREEN_X, 16], 0)
    pygame.draw.rect(
        SCREEN, [
            255, 255, 255], [
            0, SCREEN_Y - 16, SCREEN_X, SCREEN_Y], 0)
    point = ''
    if middle_key == 0:
        tips = ''
    if coordinate_click_point != [0, 0, 0]:
        a = []
        for i in coordinate_click_point:
            if i != 0:
                a.append(i)
        point += f'坐标端点:{str(a)}  '
    if line:
        point += f'端点:{str(line)}  '
    if rect:
        point += f'顶点(圆心):{str(rect)}  '
    if poly:
        point += f'多顶点:{str(poly)}  '
    if continuous_draw or middle_key != 0:
        model_tip = FONT.render(
            f'模式:{key_d} , {mode[middle_key]} {tips}', True, (0, 0, 0))
    else:
        s = ''
        if save_dir:
            s = f'保存路径（w）:{save_dir}'
        model_tip = FONT.render(
            f'{time.strftime("%Y/%m/%d  %I:%M")}  {s}', True, (0, 0, 0))
        point = ''
    if point == '':
        point = f'主色调:{pen_color} 增函数颜色:{increasing_color} 减函数颜色:{subtraction_color}'
    mouse_tip = FONT.render(f'鼠标:{bottom_tip[0]},{bottom_tip[1]}', True, (0, 0, 0))
    status_tip = FONT.render(
        f'{bottom_tip[2]},{bottom_tip[3]},{bottom_tip[4]} ; 大小:{pen_weight} ; '
        f'原点:{record_origin_x},{record_origin_y}'
        f' ; 跨度:{span} ; {point}',
        True,
        (0,
         0,
         0))
    SCREEN.blit(mouse_tip, (0, 0))
    SCREEN.blit(status_tip, (100, 0))
    SCREEN.blit(model_tip, (0, SCREEN_Y - 16))


def draw_main(in_queue, out_queue):
    global previous_x, previous_y, pen_color, pen_weight, coordinate_system_drawing_method
    global coordinate_click_point, record_origin_x
    global record_origin_y, span, line
    global continuous_draw, middle_key, rect, poly, SCREEN, SCREEN_CAPTION, init_done, previous_x, previous_y, save_dir
    global increasing_color, subtraction_color, bottom_tip, FONT, SCREEN_X, SCREEN_Y, tips
    start_gui()
    queue_controller.set_queue(in_queue, out_queue)
    queue_controller()
    flat = True  # 循环条件（不是全局）
    while flat:
        top_draw()
        pygame.display.update()  # 屏幕刷新
        for event in pygame.event.get():  # 事件检查
            if event.type == QUIT:  # 退出事件
                pygame.quit()
                flat = False
                break
            elif event.type == MOUSEMOTION:  # 鼠标移动事件
                bottom_tip[0], bottom_tip[1] = event.pos
                bottom_tip[2], bottom_tip[3], bottom_tip[4] = event.buttons
                if event.buttons == (1, 0, 0):  # 左键点击
                    draw_line(event.pos)
                elif event.buttons == (0, 0, 0):  # 无点击绘图（启动快捷键d）
                    if continuous_draw:
                        draw_line(event.pos)
                    else:  # m_x和m_y是指上一点的xy，用于画线系统
                        previous_x = None
                        previous_y = None
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按下
                event.pos = list(event.pos)
                if event.button == 3:  # 右键点击
                    bottom_tip[4] = 1
                    pygame.image.save(SCREEN, '$CoTanCC.png')  # 保存当前环境
                    SCREEN = pygame.display.set_mode(
                        (SCREEN_X, SCREEN_Y), pygame.NOFRAME)  # 隐藏关闭按钮
                    background_image = pygame.image.load('$CoTanCC.png').convert()  # 加载位图
                    SCREEN.blit(background_image, (0, 0))  # 绘制位图
                    pygame.display.update()  # 更新屏幕
                    tool_set = tool_box()  # 启动工具箱
                    SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0)  # 显示关闭按钮
                    background_image = pygame.image.load('$CoTanCC.png').convert()  # 加载位图
                    SCREEN.blit(background_image, (0, 0))  # 绘制位图
                    pygame.display.update()  # 更新屏幕
                    os.remove('$CoTanCC.png')
                    if tool_set[0] is not None:
                        pen_color = tool_set[0]  # 设置颜色
                    if tool_set[1] is not None:
                        pen_weight = tool_set[1]  # 设置笔的粗细
                    if tool_set[2] is not None:
                        SCREEN.fill(tool_set[2])  # 设置背景填充
                    if tool_set[3] == 1:  # 绘制坐标系
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        coordinate_system_drawing_method = 3
                        span = 60
                    elif tool_set[3] == 2:  # 绘制坐标系2（小跨度）
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        coordinate_system_drawing_method = 3
                        span = 20
                    elif tool_set[3] == 3:  # 绘制坐标系3（大跨度）
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        coordinate_system_drawing_method = 3
                        span = 120  # 坐标系跨度（字定义跨度再下面）
                    else:
                        middle_key = 0
                        coordinate_system_drawing_method = 0  # 恢复选项
                    if tool_set[6] is not None:
                        increasing_color = tool_set[6]  # 增函数颜色（要在函数绘制之前设置好）
                    if tool_set[7] is not None:
                        subtraction_color = tool_set[7]  # 减函数颜色
                    if tool_set[4] != {}:
                        func_draw(tool_set[4])  # 函数绘制
                    if tool_set[5] is not None:
                        pygame.image.save(SCREEN, tool_set[5])  # 保存当前环境
                        save_dir = tool_set[5]
                    if tool_set[8] is not None:
                        span = tool_set[8]  # 自定义跨度
                    if tool_set[9] is not None:
                        try:
                            bg_im = pygame.image.load(tool_set[9]).convert()  # 加载位图
                            SCREEN.blit(bg_im, (0, 0))  # 绘制位图
                        except BaseException as e:
                            logging.warning(str(e))
                    # 恢复参数
                    previous_x = None
                    previous_y = None
                    continuous_draw = False
                    pygame.event.clear()
                elif event.button == 2:  # 中键点击，ZJ是指中键的模式，来自快捷键和工具箱
                    bottom_tip[3] = 1
                    if middle_key == 1:  # 坐标系模式
                        tips = '选择下一个端点（共3个）'
                        coordinate_click_point[coordinate_system_drawing_method - 1] = event.pos  # 存储
                        coordinate_system_drawing_method -= 1
                        if coordinate_system_drawing_method == 0:
                            x = []
                            y = []
                            for i in coordinate_click_point:
                                x.append(i[0])
                                y.append(i[1])
                            x.sort()
                            y.sort()  # 排序
                            s_x = x[1]
                            s_y = y[1]
                            p = (-abs(x[0] - x[1]), abs(x[1] - x[2]))
                            c = (-abs(y[0] - y[1]), abs(y[1] - y[2]))
                            b = 2 * pen_weight
                            r = 2 * pen_weight
                            jt = 3 * pen_weight
                            coordinate_draw(s_x, s_y, p, c, span, b, jt, r)
                            coordinate_click_point = [0, 0, 0]
                            middle_key = 0
                    elif middle_key == 2:  # 画线模式
                        line.append(event.pos)
                        # pygame.draw.circle(root, pen_C, event.pos, d, 0)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], line[1], pen_weight)
                            middle_key = 0
                    elif middle_key == 3 or middle_key == 4:  # 画矩形模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort()
                            y.sort()
                            if middle_key == 3:
                                dx = 0
                            else:
                                dx = pen_weight
                            pygame.draw.rect(
                                SCREEN, pen_color, [
                                    x[0], y[0], x[1] - x[0], y[1] - y[0]], dx)
                            middle_key = 0
                    elif middle_key == 5:  # 画横线模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[1][0], line[0][1]), pen_weight)
                            middle_key = 0
                    elif middle_key == 6:  # 画竖线模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[0][0], line[1][1]), pen_weight)
                            middle_key = 0
                    elif middle_key == 7:  # 画线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], line[1], pen_weight)
                            del line[0]
                    elif middle_key == 8:  # 画横线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[1][0], line[0][1]), pen_weight)
                            pygame.draw.circle(
                                SCREEN, pen_color, (line[1][0], line[0][1]), pen_weight * 2, 0)
                            del line[1]
                        else:
                            pygame.draw.circle(
                                SCREEN, pen_color, event.pos, pen_weight, 0)
                    elif middle_key == 9:  # 画竖线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[0][0], line[1][1]), pen_weight)
                            pygame.draw.circle(
                                SCREEN, pen_color, (line[0][0], line[1][1]), pen_weight * 2, 0)
                            del line[1]
                        else:
                            pygame.draw.circle(
                                SCREEN, pen_color, event.pos, pen_weight, 0)
                    elif middle_key == 10:  # 画竖线和横线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[1][0], line[0][1]), pen_weight)  # 横线
                            pygame.draw.circle(
                                SCREEN, pen_color, (line[1][0], line[0][1]), pen_weight * 2, 0)
                            pygame.draw.circle(
                                SCREEN, pen_color, (line[1][0], line[1][1]), pen_weight * 2, 0)
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], (line[0][0], line[1][1]), pen_weight)  # 竖线
                            pygame.draw.circle(
                                SCREEN, pen_color, (line[0][0], line[1][1]), pen_weight * 2, 0)
                            # 垂直于横线的虚线
                            p = sorted([line[1][1], line[0][1]])
                            y1 = p[0]
                            y2 = p[1]
                            a = list(range(y1, y2, 10))
                            for i in range(
                                    int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                i += 1
                                i = 2 * i - 1
                                y1 = a[i - 1]  # 计算两点的y坐标
                                y2 = a[i]
                                pygame.draw.line(
                                    SCREEN, pen_color, (line[1][0], y1), (line[1][0], y2), pen_weight)  # 横线
                            # 垂直于竖线的虚线
                            p = [line[1][0], line[0][0]]
                            p.sort()
                            x1 = p[0]
                            x2 = p[1]
                            a = list(range(x1, x2, 10))
                            for i in range(
                                    int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                i += 1
                                i = 2 * i - 1
                                x1 = a[i - 1]  # 计算两点的x坐标
                                x2 = a[i]
                                pygame.draw.line(
                                    SCREEN, pen_color, (x1, line[1][1]), (x2, line[1][1]), pen_weight)  # 横线
                            del line[1]
                        else:
                            pygame.draw.circle(
                                SCREEN, pen_color, event.pos, pen_weight, 0)
                    elif middle_key == 11:  # 画虚线线模式
                        line.append(event.pos)
                        pygame.draw.circle(
                            SCREEN, pen_color, event.pos, pen_weight, 0)
                        if len(line) == 2:
                            if abs(line[0][0] - line[1][0]) >= 100:
                                p1 = [line[0][0], line[1][0]]
                                p2 = {
                                    line[0][0]: line[0][1],
                                    line[1][0]: line[1][1]}
                                p1.sort()
                                x1 = p1[0]
                                y1 = p2[x1]
                                x2 = p1[1]
                                y2 = p2[x2]
                                a = list(range(x1, x2, 10))
                                for i in range(
                                        int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                    i += 1
                                    i = 2 * i - 1
                                    x1 = a[i - 1]  # 计算两点的x坐标
                                    x2 = a[i]
                                    y1 = (x1 - x1) / (x2 - x1) * (y2 - y1) + y1
                                    y2 = (x2 - x1) / (x2 - x1) * (y2 - y1) + y1
                                    pygame.draw.line(
                                        SCREEN, pen_color, (x1, y1), (x2, y2), pen_weight)  # 横线
                            elif abs(line[0][1] - line[1][1]) >= 100:
                                p1 = [line[0][1], line[1][1]]
                                p2 = {
                                    line[0][1]: line[0][0],
                                    line[1][1]: line[1][0]}
                                p1.sort()
                                y1 = p1[0]
                                x1 = p2[y1]
                                y2 = p1[1]
                                x2 = p2[y2]
                                a = list(range(y1, y2, 10))
                                for i in range(
                                        int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                    i += 1
                                    i = 2 * i - 1
                                    y1 = a[i - 1]  # 计算两点的x坐标
                                    y2 = a[i]
                                    x1 = (y1 - y1) / (y2 - y1) * (x2 - x1) + x1
                                    x2 = (y2 - y1) / (y2 - y1) * (x2 - x1) + x1
                                    pygame.draw.line(
                                        SCREEN, pen_color, (x1, y1), (x2, y2), pen_weight)  # 横线
                            else:
                                pygame.draw.line(
                                    SCREEN, pen_color, line[1], line[0], pen_weight)
                            middle_key = 0
                    elif middle_key == 12:  # 画圆模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            # 两点间求距离
                            r = int(
                                ((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2) ** (1 / 2))
                            pygame.draw.circle(SCREEN, pen_color, rect[0], r, 0)
                            middle_key = 0
                        else:
                            pygame.draw.circle(
                                SCREEN, pen_color, rect[0], pen_weight * 2, 0)
                    elif middle_key == 13:  # 画圆线框模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            # 两点间求距离
                            r = int(
                                ((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2) ** (1 / 2))
                            pygame.draw.circle(
                                SCREEN, pen_color, rect[0], r, pen_weight)
                            middle_key = 0
                        else:
                            pygame.draw.circle(
                                SCREEN, pen_color, rect[0], pen_weight, 0)
                    elif middle_key == 14:  # 画多边形模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(
                                SCREEN, pen_color, line[0], line[1], pen_weight)
                            del line[0]
                        poly.append(event.pos)
                    elif middle_key == 15:  # 画椭圆模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort()
                            y.sort()
                            pygame.draw.ellipse(
                                SCREEN, pen_color, [
                                    x[0], y[0], x[1] - x[0], y[1] - y[0]], 0)
                            middle_key = 0
                    elif middle_key == 16:  # 画椭圆边框模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort()
                            y.sort()
                            pygame.draw.ellipse(
                                SCREEN, pen_color, [
                                    x[0], y[0], x[1] - x[0], y[1] - y[0]], pen_weight)
                            middle_key = 0
                elif event.button == 1:
                    bottom_tip[2] = 1
                    pygame.draw.circle(
                        SCREEN, pen_color, event.pos, pen_weight, 0)
                    previous_x = event.pos[0]
                    previous_y = event.pos[1]
            elif event.type == KEYDOWN:  # 键盘按下（长按不算）快捷键
                if event.key == K_d:  # 不用点击左键画线
                    if continuous_draw:
                        continuous_draw = False
                    else:
                        continuous_draw = True
                        previous_x = None
                        previous_y = None
                elif event.key == K_g:  # 画直线
                    tips = '根据两个端点画直线'
                    middle_key = 2
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_f:  # 画矩阵
                    middle_key = 3
                    tips = '根据两个相对的顶点绘制矩形'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_s:  # 画矩阵边框
                    middle_key = 4
                    tips = '根据两个相对的顶点绘制矩形'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_k:  # 画横线
                    middle_key = 5
                    tips = '选择起点和与终点y坐标相同的点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_l:  # 画竖线
                    middle_key = 6
                    tips = '选择起点和与终点x坐标相同的点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_j:  # 多段线
                    if middle_key == 7:
                        middle_key = 0
                    else:
                        middle_key = 7
                        tips = '依次选择多段线的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_i:  # 多段线横线打点
                    if middle_key == 8:
                        middle_key = 0
                    else:
                        middle_key = 8
                        tips = '选择终点，依次选择与其他端点y坐标相同的点（点击i结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_u:  # 多段线竖线打点
                    if middle_key == 9:
                        middle_key = 0
                    else:
                        middle_key = 9
                        tips = '选择终点，依次选择与其他端点x坐标相同的点（点击u结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_h:  # 多段横竖线打点
                    if middle_key == 10:
                        middle_key = 0
                    else:
                        middle_key = 10
                        tips = '选择参考点，再选择研究对象（点击h结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_q:  # 绘制虚线
                    middle_key = 11
                    tips = '选择虚线的两个端点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_c:  # 绘制圆形
                    middle_key = 12
                    tips = '选择圆形和圆上任意一点（确定半径）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_v:  # 绘制圆形线框
                    middle_key = 13
                    tips = '选择圆形和圆上任意一点（确定半径）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_o:  # 捕捉
                    tips = '起点已经捕捉到坐标系原点了'
                    line = [[record_origin_x, record_origin_y]]
                    rect = [[record_origin_x, record_origin_y]]
                    poly = [[record_origin_x, record_origin_y]]
                elif event.key == K_y:  # 捕捉上y轴
                    if len(line) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        line[0][0] = record_origin_x
                    if len(rect) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        rect[0][0] = record_origin_x
                    if len(poly) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        rect[0][0] = record_origin_x
                elif event.key == K_x:  # 捕捉上x轴
                    if len(line) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        line[0][1] = record_origin_y
                    if len(rect) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        rect[0][1] = record_origin_y
                    if len(poly) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        rect[0][1] = record_origin_y
                elif event.key == K_n:  # 画多边形
                    if middle_key == 14:
                        middle_key = 0
                        pygame.draw.polygon(SCREEN, pen_color, poly, 0)
                    else:
                        tips = '依次选择多边形的各个端点(点击n闭合并填充)'
                        middle_key = 14
                elif event.key == K_m:  # 画多边形边框
                    if middle_key == 14:
                        middle_key = 0
                        pygame.draw.polygon(SCREEN, pen_color, poly, pen_weight)
                    else:
                        tips = '依次选择多边形的各个端点(点击m闭合)'
                        middle_key = 14
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_e:  # 绘制填充椭圆
                    middle_key = 15
                    tips = '选择椭圆外界矩形的两个相对的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_r:  # 绘制椭圆边框
                    middle_key = 16
                    tips = '选择椭圆外界矩形的两个相对的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_w:  # 保存
                    if save_dir != '':
                        pygame.image.save(SCREEN, save_dir)  # 保存当前环境
                elif event.key == K_b:  # 清空当前操作
                    middle_key = 0
                    line = []
                    rect = []
                    poly = []
    queue_controller.stop_process()

# 快捷键操作指南
# d-不用点击左键画线（再次点击关闭）
# g-画直线
# f-画填充矩阵
# s-画矩阵边框
# k-画横线
# l-画竖线
# j-画多段线
# i-横线多段线打点（再次点击结束绘制）
# u-竖线多段线打点（再次点击结束绘制）
# h-横线和竖线多段线打点并由虚线标注（再次点击结束绘制）
# q-绘制虚线
# c-绘制填充圆形
# v-绘制圆形边框
# n和m-绘制多边形
# n-再次点击完成填充多边形绘制
# m-再次点击完成多边形边框绘制
# o-捕捉坐标原点（请先点击功能快捷键）
# x-捕捉坐标x轴（请先点击功能快捷键并选择起点）
# y-捕捉坐标y轴（同上）
# b-关闭当前所有快捷键操作
# e-绘制填充椭圆
# r-绘制椭圆边框
