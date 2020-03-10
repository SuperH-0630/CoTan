import pygame
from pygame.locals import *
from CGB.TK import tool_box
import time
import os

#定义一些变量
PEN_C = [0, 0, 0]  # 画笔颜色
Z_C = [0,0,255]
J_C = [255,0,0]
PEN_THICKNESS = 2  # 圆形的粗细（线条*2）=中笔
m_x = None
m_y = None  # 为画图所准备的
continuous_draw = False  # 设置免按
XY = 0
axy = [0, 0, 0]  # 坐标系
XY_x = 0
XY_y = 0  # 原点坐标
X_P = []  # X点
Y_C = []  # Y点
X_L = []  # X个数
Y_L = []  # Y个数
X_M = []
Y_M = []
_span = 60  # 坐标系跨度调节

middle_key = 0  # 中键模式
line = []  # 画线列表
rect = []  # 画矩阵和圆列表
poly = []  # 画多边形列表

tips = ''#设置备注

BC_Dic = ''#保存路径
Tip = [0,0,0,0,0]#底部显示信息[x,y,左键，中间，右键]

mode = {1: '绘制坐标系', 2: '绘制直线(g)', 3: '填充矩形(f)', 4: '线条矩形(s)',
        5:'绘制横线(k)', 6:'绘制竖线(l)', 7:'绘制多段线(j)',
        8:'绘制横打点多段线(i)', 9:'绘制竖打点多段线(u)', 10:'坐标测绘(h)',
        11:'绘制虚线(q)', 12:'填充圆形(c)', 13:'线条圆形(v)', 14:'多边形(n-填充,m-线条)',
        15:'填充椭圆形(e)', 16:'线条椭圆形(r)', 0:'None'}#快捷键名字

#绘制函数
def func_draw(HS_list, JD = 1000):
    global X_P,X_L,Y_C,Y_L,Y_M,X_M,PEN_C,Z_C,J_C
    c = [0,0,0]#增函数颜色
    X_Done = lambda x: (x - X_L[0]) / (X_L[1] - X_L[0]) * (X_P[1] - X_P[0]) + X_P[0]#x是数值,换算为像素
    Y_Done = lambda y: (y - Y_L[0]) / (Y_L[1] - Y_L[0]) * (Y_C[1] - Y_C[0]) + Y_C[0]  # x是数值,换算为像素
    for i in HS_list:
        x1 = None  # 上一组X和Y
        y1 = None
        if HS_list == None:continue
        D = HS_list[i]
        try:
            for x in range((X_L[0]-1)*JD,(X_L[1]+1)*JD,1):
                x /= JD
                try:
                    y = D(x)
                except:
                    x1 = None
                    y1 = None
                    continue
                try:
                    x2 = X_Done(x)
                    y2 = Y_Done(y)
                    if y2>Y_M[0] or y2<Y_M[1] or x2<X_M[0] or x2>X_M[1]:
                        x1 = None
                        y1 = None
                        continue
                except TypeError:#预防复数
                    continue
                if x1 != None:
                    if y1>y2:c=Z_C#增函数
                    elif y1<y2:c=J_C#减函数#改为检查Y数值而不是坐标
                    pygame.draw.line(root, c, (int(x1),int(y1)), (int(x2),int(y2)), PEN_THICKNESS)
                x1 = x2
                y1 = y2
        except IndexError:
            break

#画曲线系统
def draw_line(xy, c=False):#c-是否带点
    global m_x,m_y
    if c:pygame.draw.circle(root, PEN_C, xy, PEN_THICKNESS, 0)
    if m_x != None:
        pygame.draw.line(root, PEN_C, (m_x, m_y), xy, PEN_THICKNESS)
    m_x = xy[0]
    m_y = xy[1]

#绘制XY坐标系
def coordinate_draw(s_x, s_y, p = (-100, 100), c = (-200, 100), kd = 10, b = 3, jt = 3, r = 3):
    kd = abs(kd)#kd大于0
    global PEN_THICKNESS,XY_x,XY_y,X_L,X_P,Y_L,Y_C,X_M,Y_M
    XY_x = s_x
    XY_y = s_y#存储原点坐标
    X_M = [s_x + p[0],s_x + p[1]]
    Y_M = [s_y + c[1],s_y + c[0]]
    pygame.draw.circle(root, PEN_C, (s_x, s_y), r, 0)#绘制原点
    pygame.draw.line(root, PEN_C, (s_x + p[0], s_y), (s_x + p[1], s_y), PEN_THICKNESS)  # X轴，Y定
    pygame.draw.line(root, PEN_C, (s_x, s_y + c[0]), (s_x, s_y + c[1]), PEN_THICKNESS)  # y轴，x定
    _a = 0#刻度统计
    _c = 0
    for i in range(s_x ,s_x + p[0], -kd):#右
        _a -= 1
        pygame.draw.line(root, PEN_C, (i, s_y + b), (i, s_y), PEN_THICKNESS)
        _c = i
    _b = 0
    _d = 0
    for i in range(s_x, s_x + p[1], kd):#刻度#左
        _b += 1
        pygame.draw.line(root, PEN_C, (i, s_y + b), (i, s_y), PEN_THICKNESS)
        _d = i
    X_L = [_a+1,_b-1]
    X_P = [_c,_d]
    _a = 0
    _c = 0
    for i in range(s_y, s_y + c[0], -kd):#上
        _a += 1
        pygame.draw.line(root, PEN_C, (s_x + b, i), (s_x, i), PEN_THICKNESS)
        _c = i
    _b = 0
    _d = 0
    for i in range(s_y, s_y + c[1], kd):#下
        _b -= 1
        pygame.draw.line(root, PEN_C, (s_x + b, i), (s_x, i), PEN_THICKNESS)
        _d = i
    Y_L = [_b+1,_a-1]
    Y_C = [_d,_c]

    #箭头
    pygame.draw.line(root, PEN_C, (s_x + p[1], s_y), (s_x + p[1] - jt, s_y + jt), PEN_THICKNESS)  # X上
    pygame.draw.line(root, PEN_C, (s_x + p[1], s_y), (s_x + p[1] - jt, s_y - jt), PEN_THICKNESS)  # X下

    pygame.draw.line(root, PEN_C, (s_x, s_y + c[0]), (s_x - jt, s_y + c[0] + jt), PEN_THICKNESS)  # y左
    pygame.draw.line(root, PEN_C, (s_x, s_y + c[0]), (s_x + jt, s_y + c[0] + jt), PEN_THICKNESS)  # X下

def top_draw():
    #绘制顶部
    global PEN_THICKNESS,Font,Tip,Screen_x,Screen_y,middle_key,BC_Dic,mode,continuous_draw,XY_x,XY_y,tips,line,rect,poly,PEN_C,Z_C,J_C,axy,_span
    if continuous_draw:mod_d = '启动无点击画线(点击d关闭)'
    else:mod_d = '关闭无点击画线'
    pygame.draw.rect(root,[255,255,255], [0,0,Screen_x,16], 0)
    pygame.draw.rect(root, [255, 255, 255], [0, Screen_y-16, Screen_x, Screen_y], 0)
    p = ''
    if middle_key == 0: tips = ''
    if axy != [0,0,0]:
        a = []
        for i in axy:
            if i != 0:a.append(i)
        p += f'坐标端点:{str(a)}  '
    if line:
        p += f'端点:{str(line)}  '
    if rect:
        p += f'顶点(圆心):{str(rect)}  '
    if poly:
        p += f'多顶点:{str(poly)}  '
    if continuous_draw or middle_key != 0:
        TIP3 = Font.render(f'模式:{mod_d} , {mode[middle_key]} {tips}', True, (0, 0, 0))
    else:
        s = ''
        if BC_Dic:s = f'保存路径（w）:{BC_Dic}'
        TIP3 = Font.render(f'{time.strftime("%Y/%m/%d  %I:%M")}  {s}', True, (0, 0, 0))
        p = ''
    if p == '':
        p = f'主色调:{PEN_C} 增函数颜色:{Z_C} 减函数颜色:{J_C}'
    TIP = Font.render(f'鼠标:{Tip[0]},{Tip[1]}',True, (0, 0, 0))
    TIP2 = Font.render(f'{Tip[2]},{Tip[3]},{Tip[4]} ; 大小:{PEN_THICKNESS} ; 原点:{XY_x},{XY_y} ; 跨度:{_span} ; {p}', True, (0, 0, 0))
    root.blit(TIP, (0, 0))
    root.blit(TIP2, (100, 0))
    root.blit(TIP3, (0, Screen_y - 16))

#主程序
def draw_main(dis_x=900, dis_y=700):
    global m_x, m_y,PEN_C,PEN_THICKNESS,BG,XY,axy,XY_x,XY_y,_span,line,continuous_draw,middle_key,rect,poly,root,root_caption,done,m_x, m_y,BC_Dic#定义全局变量
    global Z_C,J_C,Tip,Font,Screen_x,Screen_y,tips,Font
    Screen_x = dis_x
    Screen_y = dis_y
    done = pygame.init()  # 初始化所有模块
    if done[1] != 0: print('Init!')  # 检查是否错误
    Font = pygame.font.Font('Font\ZKST.ttf', 16)  # 设置字体(Linux下应该用\而不是/)
    root = pygame.display.set_mode((dis_x, dis_y),0)  # 创建屏幕
    root_caption = pygame.display.set_caption('CoTan草稿板')#定义标题（后期加上定义Logo）
    root.fill([255, 255, 255])  # 默认用白色填充窗口
    flat = True#循环条件（不是全局）
    while flat:
        top_draw()
        pygame.display.update()#屏幕刷新
        for event in pygame.event.get():#事件检查
            if event.type == QUIT:#退出事件
                pygame.quit()
                flat = False
                break
            elif event.type == MOUSEMOTION:#鼠标移动事件
                Tip[0],Tip[1] = event.pos
                Tip[2],Tip[3],Tip[4] = event.buttons
                if event.buttons == (1, 0, 0):#左键点击
                    draw_line(event.pos)
                elif event.buttons == (0, 0, 0):#无点击绘图（启动快捷键d）
                    if continuous_draw:
                        draw_line(event.pos)
                    else:#m_x和m_y是指上一点的xy，用于画线系统
                        m_x = None
                        m_y = None
            elif event.type == MOUSEBUTTONDOWN:#鼠标按下
                event.pos = list(event.pos)
                if event.button == 3:#右键点击
                    Tip[4] = 1
                    pygame.image.save(root,'$CoTanCC.png')#保存当前环境
                    root = pygame.display.set_mode((dis_x, dis_y), pygame.NOFRAME)#隐藏关闭按钮
                    bg = pygame.image.load('$CoTanCC.png').convert()#加载位图
                    root.blit(bg, (0, 0))#绘制位图
                    pygame.display.update()#更新屏幕
                    g = tool_box()#启动工具箱
                    root = pygame.display.set_mode((dis_x, dis_y), 0)#显示关闭按钮
                    bg = pygame.image.load('$CoTanCC.png').convert()#加载位图
                    root.blit(bg, (0, 0))#绘制位图
                    pygame.display.update()#更新屏幕
                    os.remove('$CoTanCC.png')
                    if g[0] != None:PEN_C = g[0]#设置颜色
                    if g[1] != None:PEN_THICKNESS = g[1]#设置笔的粗细
                    if g[2] != None: root.fill(g[2])#设置背景填充
                    if g[3] == 1:#绘制坐标系
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        XY = 3
                        _span = 60
                    elif g[3] == 2:#绘制坐标系2（小跨度）
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        XY = 3
                        _span = 20
                    elif g[3] == 3:#绘制坐标系3（大跨度）
                        tips = '选择坐标三个端点'
                        middle_key = 1
                        XY = 3
                        _span = 120#坐标系跨度（字定义跨度再下面）
                    else:
                        middle_key = 0
                        XY = 0#恢复选项
                    if g[6] != None: Z_C = g[6]  # 增函数颜色（要在函数绘制之前设置好）
                    if g[7] != None: J_C = g[7]  # 减函数颜色
                    if g[4] != {}:func_draw(g[4])#函数绘制
                    if g[5] != None:
                        pygame.image.save(root, g[5])  # 保存当前环境
                        BC_Dic = g[5]
                    if g[8] != None: _span = g[8]  # 自定义跨度
                    if g[9] != None:
                        try:
                            bg_im = pygame.image.load(g[9]).convert()  # 加载位图
                            root.blit(bg_im, (0, 0))  # 绘制位图
                        except:pass
                    #恢复参数
                    m_x = None
                    m_y = None
                    continuous_draw = False
                    pygame.event.clear()
                elif event.button == 2:#中键点击，ZJ是指中键的模式，来自快捷键和工具箱
                    Tip[3] = 1
                    if middle_key == 1:#坐标系模式
                        tips = '选择下一个端点（共3个）'
                        axy[XY-1] = event.pos#存储
                        XY -= 1
                        if XY == 0:
                            x = []
                            y = []
                            for i in axy:
                                x.append(i[0])
                                y.append(i[1])
                            x.sort()
                            y.sort()#排序
                            s_x = x[1]
                            s_y = y[1]
                            p = (-abs(x[0] - x[1]), abs(x[1] - x[2]))
                            c = (-abs(y[0] - y[1]), abs(y[1] - y[2]))
                            b = 2 * PEN_THICKNESS
                            r = 2 * PEN_THICKNESS
                            jt = 3 * PEN_THICKNESS
                            coordinate_draw(s_x, s_y, p, c, _span, b, jt, r)
                            axy = [0,0,0]
                            middle_key = 0
                    elif middle_key == 2:#画线模式
                        line.append(event.pos)
                        # pygame.draw.circle(root, pen_C, event.pos, d, 0)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], line[1], PEN_THICKNESS)
                            middle_key = 0
                    elif middle_key == 3 or middle_key == 4:#画矩形模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort();y.sort()
                            if middle_key == 3:dx = 0
                            else:dx = PEN_THICKNESS
                            pygame.draw.rect(root, PEN_C, [x[0], y[0], x[1] - x[0], y[1] - y[0]], dx)
                            middle_key = 0
                    elif middle_key == 5:#画横线模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], (line[1][0], line[0][1]), PEN_THICKNESS)
                            middle_key = 0
                    elif middle_key == 6:#画竖线模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], (line[0][0], line[1][1]), PEN_THICKNESS)
                            middle_key = 0
                    elif middle_key == 7:#画线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], line[1], PEN_THICKNESS)
                            del line[0]
                    elif middle_key == 8:#画横线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], (line[1][0], line[0][1]), PEN_THICKNESS)
                            pygame.draw.circle(root, PEN_C, (line[1][0], line[0][1]), PEN_THICKNESS * 2, 0)
                            del line[1]
                        else:
                            pygame.draw.circle(root, PEN_C, event.pos, PEN_THICKNESS, 0)
                    elif middle_key == 9:#画竖线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], (line[0][0], line[1][1]), PEN_THICKNESS)
                            pygame.draw.circle(root, PEN_C, (line[0][0], line[1][1]), PEN_THICKNESS * 2, 0)
                            del line[1]
                        else:
                            pygame.draw.circle(root, PEN_C, event.pos, PEN_THICKNESS, 0)
                    elif middle_key == 10:#画竖线和横线多段线
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], (line[1][0], line[0][1]), PEN_THICKNESS)#横线
                            pygame.draw.circle(root, PEN_C, (line[1][0], line[0][1]), PEN_THICKNESS * 2, 0)
                            pygame.draw.circle(root, PEN_C, (line[1][0], line[1][1]), PEN_THICKNESS * 2, 0)
                            pygame.draw.line(root, PEN_C, line[0], (line[0][0], line[1][1]), PEN_THICKNESS)#竖线
                            pygame.draw.circle(root, PEN_C, (line[0][0], line[1][1]), PEN_THICKNESS * 2, 0)
                            #垂直于横线的虚线
                            p = [line[1][1], line[0][1]]
                            p.sort()
                            Y1 = p[0]
                            Y2 = p[1]
                            a = list(range(Y1, Y2, 10))
                            for i in range(int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                i += 1
                                i = 2 * i - 1
                                y1 = a[i - 1]  # 计算两点的y坐标
                                y2 = a[i]
                                pygame.draw.line(root, PEN_C, (line[1][0], y1), (line[1][0], y2), PEN_THICKNESS)  # 横线
                            # 垂直于竖线的虚线
                            p = [line[1][0], line[0][0]]
                            p.sort()
                            X1 = p[0]
                            X2 = p[1]
                            a = list(range(X1, X2, 10))
                            for i in range(int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                i += 1
                                i = 2 * i - 1
                                x1 = a[i - 1]  # 计算两点的x坐标
                                x2 = a[i]
                                pygame.draw.line(root, PEN_C, (x1, line[1][1]), (x2, line[1][1]), PEN_THICKNESS)  # 横线
                            del line[1]
                        else:
                            pygame.draw.circle(root, PEN_C, event.pos, PEN_THICKNESS, 0)
                    elif middle_key == 11:#画虚线线模式
                        line.append(event.pos)
                        pygame.draw.circle(root, PEN_C, event.pos, PEN_THICKNESS, 0)
                        if len(line) == 2:
                            if abs(line[0][0] - line[1][0]) >= 100:
                                p1 = [line[0][0], line[1][0]]
                                p2 = {line[0][0]:line[0][1], line[1][0]:line[1][1]}
                                p1.sort()
                                X1 = p1[0]
                                Y1 = p2[X1]
                                X2 = p1[1]
                                Y2 = p2[X2]
                                a = list(range(X1, X2, 10))
                                for i in range(int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                    i += 1
                                    i = 2 * i - 1
                                    x1 = a[i - 1]  # 计算两点的x坐标
                                    x2 = a[i]
                                    y1 = (x1 - X1) / (X2 - X1) * (Y2 - Y1) + Y1
                                    y2 = (x2 - X1) / (X2 - X1) * (Y2 - Y1) + Y1
                                    pygame.draw.line(root, PEN_C, (x1, y1), (x2, y2), PEN_THICKNESS)  # 横线
                            elif abs(line[0][1] - line[1][1]) >= 100:
                                p1 = [line[0][1], line[1][1]]
                                p2 = {line[0][1]: line[0][0], line[1][1]: line[1][0]}
                                p1.sort()
                                Y1 = p1[0]
                                X1 = p2[Y1]
                                Y2 = p1[1]
                                X2 = p2[Y2]
                                a = list(range(Y1, Y2, 10))
                                for i in range(int(len(a) / 2)):  # 向下取整，可用math.ceil代替
                                    i += 1
                                    i = 2 * i - 1
                                    y1 = a[i - 1]  # 计算两点的x坐标
                                    y2 = a[i]
                                    x1 = (y1 - Y1) / (Y2 - Y1) * (X2 - X1) + X1
                                    x2 = (y2 - Y1) / (Y2 - Y1) * (X2 - X1) + X1
                                    pygame.draw.line(root, PEN_C, (x1, y1), (x2, y2), PEN_THICKNESS)  # 横线
                            else:
                                pygame.draw.line(root, PEN_C, line[1], line[0], PEN_THICKNESS)
                            middle_key = 0
                    elif middle_key == 12:#画圆模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            r = int(((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2) ** (1 / 2))#两点间求距离
                            pygame.draw.circle(root, PEN_C, rect[0], r, 0)
                            middle_key = 0
                        else:
                            pygame.draw.circle(root, PEN_C, rect[0], PEN_THICKNESS * 2, 0)
                    elif middle_key == 13:#画圆线框模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            r = int(((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2) ** (1 / 2))#两点间求距离
                            pygame.draw.circle(root, PEN_C, rect[0], r, PEN_THICKNESS)
                            middle_key = 0
                        else:
                            pygame.draw.circle(root, PEN_C, rect[0], PEN_THICKNESS, 0)
                    elif middle_key == 14:  # 画多边形模式
                        line.append(event.pos)
                        if len(line) == 2:
                            pygame.draw.line(root, PEN_C, line[0], line[1], PEN_THICKNESS)
                            del line[0]
                        poly.append(event.pos)
                    elif middle_key == 15:#画椭圆模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort();y.sort()
                            pygame.draw.ellipse(root, PEN_C, [x[0], y[0], x[1] - x[0], y[1] - y[0]], 0)
                            middle_key = 0
                    elif middle_key == 16:#画椭圆边框模式
                        rect.append(event.pos)
                        if len(rect) == 2:
                            x = [rect[0][0], rect[1][0]]
                            y = [rect[0][1], rect[1][1]]
                            x.sort();y.sort()
                            pygame.draw.ellipse(root, PEN_C, [x[0], y[0], x[1] - x[0], y[1] - y[0]], PEN_THICKNESS)
                            middle_key = 0
                elif event.button == 1:
                    Tip[2] = 1
                    pygame.draw.circle(root, PEN_C, event.pos, PEN_THICKNESS, 0)
                    m_x = event.pos[0]
                    m_y = event.pos[1]
            elif event.type == KEYDOWN:#键盘按下（长按不算）快捷键
                if event.key == K_d:#不用点击左键画线
                    if continuous_draw:
                        continuous_draw = False
                    else:
                        continuous_draw = True
                        m_x = None
                        m_y = None
                elif event.key == K_g:#画直线
                    tips = '根据两个端点画直线'
                    middle_key = 2
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_f:#画矩阵
                    middle_key = 3
                    tips = '根据两个相对的顶点绘制矩形'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_s:#画矩阵边框
                    middle_key = 4
                    tips = '根据两个相对的顶点绘制矩形'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_k:#画横线
                    middle_key = 5
                    tips = '选择起点和与终点y坐标相同的点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_l:#画竖线
                    middle_key = 6
                    tips = '选择起点和与终点x坐标相同的点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_j:#多段线
                    if middle_key == 7:
                        middle_key = 0
                    else:
                        middle_key = 7
                        tips = '依次选择多段线的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_i:#多段线横线打点
                    if middle_key == 8:
                        middle_key = 0
                    else:
                        middle_key = 8
                        tips = '选择终点，依次选择与其他端点y坐标相同的点（点击i结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_u:#多段线竖线打点
                    if middle_key == 9:
                        middle_key = 0
                    else:
                        middle_key = 9
                        tips = '选择终点，依次选择与其他端点x坐标相同的点（点击u结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_h:#多段横竖线打点
                    if middle_key == 10:
                        middle_key = 0
                    else:
                        middle_key = 10
                        tips = '选择参考点，再选择研究对象（点击h结束）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_q:#绘制虚线
                    middle_key = 11
                    tips = '选择虚线的两个端点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_c:#绘制圆形
                    middle_key = 12
                    tips = '选择圆形和圆上任意一点（确定半径）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_v:#绘制圆形线框
                    middle_key = 13
                    tips = '选择圆形和圆上任意一点（确定半径）'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_o:#捕捉
                    tips = '起点已经捕捉到坐标系原点了'
                    line=[[XY_x, XY_y]]
                    rect=[[XY_x, XY_y]]
                    poly=[[XY_x, XY_y]]
                elif event.key == K_y:#捕捉上y轴
                    if len(line) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        line[0][0] = XY_x
                    if len(rect) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        rect[0][0] = XY_x
                    if len(poly) >= 1:
                        tips = '起点已经移动到坐标系y轴上了'
                        rect[0][0] = XY_x
                elif event.key == K_x:#捕捉上x轴
                    if len(line) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        line[0][1] = XY_y
                    if len(rect) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        rect[0][1] = XY_y
                    if len(poly) >= 1:
                        tips = '起点已经移动到坐标系x轴上了'
                        rect[0][1] = XY_y
                elif event.key == K_n: # 画多边形
                    if middle_key == 14:
                        middle_key = 0
                        pygame.draw.polygon(root, PEN_C, poly, 0)
                    else:
                        tips = '依次选择多边形的各个端点(点击n闭合并填充)'
                        middle_key = 14
                elif event.key == K_m: # 画多边形边框
                    if middle_key == 14:
                        middle_key = 0
                        pygame.draw.polygon(root, PEN_C, poly, PEN_THICKNESS)
                    else:
                        tips = '依次选择多边形的各个端点(点击m闭合)'
                        middle_key = 14
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_e:#绘制填充椭圆
                    middle_key = 15
                    tips = '选择椭圆外界矩形的两个相对的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_r:#绘制椭圆边框
                    middle_key = 16
                    tips = '选择椭圆外界矩形的两个相对的顶点'
                    line = []
                    rect = []
                    poly = []
                elif event.key == K_w:#保存
                    if BC_Dic != '':
                        pygame.image.save(root, BC_Dic)  # 保存当前环境
                elif event.key == K_b:#清空当前操作
                    middle_key = 0
                    line = []
                    rect = []
                    poly = []

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