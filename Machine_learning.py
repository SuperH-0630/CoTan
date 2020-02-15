import tkinter
import webbrowser
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox
import os
import chardet
from tkinter.scrolledtext import ScrolledText
import Learn_Numpy

def Main():
    global top,ML,Form_List,PATH,bg,bbg,fg
    PATH = os.getcwd()
    Form_List = []
    ML = Learn_Numpy.Machine_Learner()

    top = tkinter.Tk()
    bg = '#FFFAFA'  # 主颜色
    bbg = '#FFFAFA'  # 按钮颜色
    fg = '#000000'  # 文字颜色
    top["bg"] = bg
    FONT = ('黑体', 11)  # 设置字体
    top.title('CoTan机器学习')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')  # 设置所在位置

    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 0

    tkinter.Button(top, bg=bbg, fg=fg, text='导入CSV', command=Add_CSV, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入Py', command=Add_Python, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导出CSV', command=to_CSV, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global name_Input
    a_y += 1
    tkinter.Label(top, text='表格名称:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    name_Input = tkinter.Entry(top, width=width_B)
    name_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除表格', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看表格', command=Show, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看单一表格', command=Show_One, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Form_BOX, Index_BOX, Column_BOX, to_HTML_Type, Seq_Input, Code_Input,str_must
    a_y += 1
    to_HTML_Type = tkinter.IntVar()  # 正，负，0
    lable = ['选项卡型', '可移动型', '自适应型']  # 复选框
    for i in range(3):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=to_HTML_Type,
                            value=i).grid(column=a_x + i, row=a_y, sticky=tkinter.W)

    str_must = tkinter.IntVar()
    a_y += 1
    tkinter.Label(top, text='编码方式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    Code_Input = tkinter.Entry(top, width=width_B)
    Code_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    buttom = tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg,
                                 text='字符串类型',
                                 variable=str_must)
    buttom.grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='CSV分隔符:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Seq_Input = tkinter.Entry(top, width=width_B)
    Seq_Input.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Form_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 10)  # 显示符号
    Form_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=10, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)


    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【机器学习】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                        columnspan=3,
                                                                                                        row=a_y,
                                                                                                        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global ML_BOX, ML_OUT,X_OUT,Y_OUT
    a_y += 1
    X_OUT = tkinter.StringVar()
    Put = tkinter.Entry(top, width=width_B * 2, textvariable=X_OUT)
    Put.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)
    Put['state'] = 'readonly'
    tkinter.Button(top, bg=bbg, fg=fg, text='选用特征集', command=set_Feature, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    Y_OUT = tkinter.StringVar()
    a_y += 1
    Put = tkinter.Entry(top, width=width_B * 2, textvariable=Y_OUT)
    Put.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)
    Put['state'] = 'readonly'
    tkinter.Button(top, bg=bbg, fg=fg, text='选用标签集', command=set_Label, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    ML_OUT = tkinter.StringVar()
    a_y += 1
    Put = tkinter.Entry(top, width=width_B * 2, textvariable=ML_OUT)
    Put.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)
    Put['state'] = 'readonly'
    tkinter.Button(top, bg=bbg, fg=fg, text='选用学习器', command=set_Learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Split_Input
    a_y += 1
    tkinter.Label(top, text='测试数据分割:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)
    Split_Input = tkinter.Entry(top, width=width_B * 2)
    Split_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    ML_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    ML_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='导入学习器', font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看数据', command=Show_Args, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除学习器', command=Del_Leaner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='训练机器', command=Fit_Learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='测试机器', command=Score_Learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='数据预测', command=Predict_Learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='单一变量特征选择', command=Add_SelectKBest, font=FONT, width=width_B, height=height_B).grid(column=a_x, row=a_y,columnspan=2,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    tkinter.Button(top, bg=bbg, fg=fg, text='映射标准化', command=Add_Mapzoom, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='方差特征选择',command=Add_Variance, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='使用学习器筛选', command=Add_SelectFrom_Model, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='模糊量化标准化', command=Add_Fuzzy_quantization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='Z-score',command=Add_Z_Score, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='离差标准化', command=Add_MinMaxScaler, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='Log变换', command=Add_LogScaler, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='atan变换',command=Add_atanScaler, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='小数定标准化', command=Add_decimalScaler, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='Sigmod变换', command=Add_sigmodScaler, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='正则化',command=Add_Regularization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='二值离散', command=Add_Binarizer, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='多值离散', command=Add_Discretization, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='独热编码',command=Add_OneHotEncoder, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='数字编码', command=Add_Label, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='缺失填充', command=Add_Missed, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='PCA降维',command=Add_PCA, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='RPCA降维', command=Add_RPCA, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='KPCA升维', command=Add_KPCA, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='LDA', command=Add_LDA, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,columnspan=3,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='线性回归', command=Add_Line, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='岭回归', command=Add_Ridge, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='Lasso', command=Add_Lasso, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='逻辑回归', command=Add_LogisticRegression, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='决策树回归',command=Add_Tree, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='决策树分类',command=Add_Tree_Class, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='朴素贝叶斯', font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='K邻近预测', command=Add_Knn, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='K邻近分类', command=Add_Knn_Class, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【学习器配置】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                        columnspan=3,
                                                                                                        row=a_y,
                                                                                                        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global Args_Learner
    a_y += 1
    Args_Learner = tkinter.Text(top, width=width_B * 3, height=height_B * 11)
    Args_Learner.grid(column=a_x, row=a_y, columnspan=3, rowspan=11,
                      sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    top.mainloop()


def Del_Leaner():
    Learn = get_Learner(True)
    set_Learne = get_Learner(False)  # 获取学习器Learner
    if set_Learne != Learn:
        ML.Del_Leaner(Learn)
    Update_Leaner()


def Show_Args():
    learner = get_Learner(True)
    if tkinter.messagebox.askokcancel('提示', f'是否将数据生成表格。\n(可绘制成散点图对比数据)'):
        Dic = asksaveasfilename(title='选择保存的CSV', filetypes=[("CSV", ".csv")])
    else:
        Dic = ''
    Data = ML.Show_Args(learner, Dic)
    title = f'CoTan数据处理 查看数据:{learner}'
    Creat_TextSheet(f'对象:{learner}\n\n{Data[0]}\n\n\n{Data[1]}', title)
    Update_BOX()


def get_Args_Learner():
    global Args_Learner
    return Args_Learner.get('0.0', tkinter.END)


def Score_Learner():
    learner = get_Learner()
    socore = ML.Score(get_Name(False,True),get_Name(False,False), learner)
    tkinter.messagebox.showinfo('测试完成', f'针对测试数据评分结果为:{socore}')


def Predict_Learner():
    learner = get_Learner()
    Data = ML.Predict(get_Name(False,True),learner)
    title = f'CoTan数据处理 学习器:{learner}'
    Creat_TextSheet(Data, title)
    Update_BOX()


def Fit_Learner():
    learner = get_Learner()
    try:
        split = float(Split_Input.get())
        if split < 0 or 1 < split: raise Exception
    except:
        split = 0.3
    socore = ML.Fit(get_Name(False,True),get_Name(False,False), learner, Text=get_Args_Learner(), split=split)
    tkinter.messagebox.showinfo('训练完成', f'针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n'
                                        f'针对测试数据评分({split * 100}%)结果为:{socore[1]}')


def set_Feature():
    global X_OUT
    X_OUT.set(get_Name())


def set_Label():
    global Y_OUT
    Y_OUT.set(get_Name())


def set_Learner():
    global ML_OUT
    ML_OUT.set(get_Learner(True))


def get_Learner(Type=False):
    global Learn_Dic, ML_BOX, ML_OUT
    if Type:
        try:
            return list(Learn_Dic.keys())[ML_BOX.curselection()[0]]
        except:
            # raise
            try:
                return list(Learn_Dic.keys)[0]
            except:
                return None
    else:
        try:
            return ML_OUT.get()
        except:
            return None

def Add_LDA():
    Add_leaner('LDA')

def Add_KPCA():
    Add_leaner('KPCA')

def Add_RPCA():
    Add_leaner('RPCA')

def Add_PCA():
    Add_leaner('PCA')

def Add_Missed():
    Add_leaner('Missed')

def Add_Label():
    Add_leaner('Label')

def Add_OneHotEncoder():
    Add_leaner('OneHotEncoder')

def Add_Discretization():
    Add_leaner('Discretization')

def Add_Binarizer():
    Add_leaner('Binarizer')

def Add_Regularization():
    Add_leaner('Regularization')

def Add_Fuzzy_quantization():
    Add_leaner('Fuzzy_quantization')

def Add_Mapzoom():
    Add_leaner('Mapzoom')

def Add_sigmodScaler():
    Add_leaner('sigmodScaler')

def Add_decimalScaler():
    Add_leaner('decimalScaler')

def Add_atanScaler():
    Add_leaner('atanScaler')

def Add_LogScaler():
    Add_leaner('LogScaler')

def Add_MinMaxScaler():
    Add_leaner('MinMaxScaler')

def Add_Z_Score():
    Add_leaner('Z-Score')

def Add_Tree_Class():
    Add_leaner('Tree_class')

def Add_Tree():
    Add_leaner('Tree')


def Add_SelectKBest():
    Add_leaner('SelectKBest')


def Add_Knn_Class():
    Add_leaner('Knn_class')


def Add_LogisticRegression():
    Add_leaner('LogisticRegression')


def Add_Lasso():
    Add_leaner('Lasso')


def Add_Variance():
    Add_leaner('Variance')


def Add_Knn():
    Add_leaner('Knn')


def Add_Ridge():
    Add_leaner('Ridge')


def Add_Line():
    Add_leaner('Line')


def Add_SelectFrom_Model():  # 添加Lenear的核心
    ML.Add_SelectFrom_Model(get_Learner(), Text=get_Args_Learner())
    Update_Leaner()


def Add_leaner(Type):  # 添加Lenear的核心
    ML.Add_Learner(Type, Text=get_Args_Learner())
    Update_Leaner()


def Update_Leaner():
    global Learn_Dic, ML_BOX
    Learn_Dic = ML.Return_Learner()
    ML_BOX.delete(0, tkinter.END)
    ML_BOX.insert(tkinter.END, *Learn_Dic.keys())


def Show_One():
    global PATH, to_HTML_Type
    Dic = f'{PATH}/$Show_Sheet.html'
    try:
        name = get_Name()
        if name == None: raise Exception
        ML.to_Html_One(name, Dic)
        webbrowser.open(Dic)
    except:
        # pass
        raise


def Show():
    global PATH, to_HTML_Type
    Dic = f'{PATH}/$Show_Sheet.html'
    try:
        name = get_Name()
        if name == None: raise Exception
        ML.to_Html(name, Dic, to_HTML_Type.get())
        webbrowser.open(Dic)
    except:
        pass


def to_CSV():
    global top, Seq_Input, Code_Input, str_must, Index_must
    Dic = asksaveasfilename(title='选择保存的CSV', filetypes=[("CSV", ".csv")])
    Seq = Seq_Input.get()
    name = get_Name()
    ML.to_CSV(Dic, name, Seq)
    Update_BOX()


def Add_CSV():
    global top, Seq_Input, Code_Input, str_must, name_Input
    Dic = askopenfilename(title='选择载入的CSV', filetypes=[("CSV", ".csv")])
    if Dic == '': return False
    Seq = Seq_Input.get()
    Codeing = Code_Input.get()
    str_ = bool(str_must.get())
    name = name_Input.get().replace(' ', '')
    if name == '':
        name = os.path.splitext(os.path.split(Dic)[1])[0]
        print(name)
    if Codeing == '':
        with open(Dic, 'rb') as f:
            Codeing = chardet.detect(f.read())['encoding']
    if Seq == '': Seq = ','
    ML.read_csv(Dic, name, Codeing, str_, Seq,)
    Update_BOX()


def Add_Python():
    global top, Seq_Input, Code_Input, str_must, Index_must
    Dic = askopenfilename(title='选择载入的py', filetypes=[("Python", ".py"), ("Txt", ".txt")])
    name = name_Input.get().replace(' ', '')
    if name == '':
        name = os.path.splitext(os.path.split(Dic)[1])[0]
    with open(Dic, 'r') as f:
        ML.Add_Python(f.read(), name)
    Update_BOX()

def get_Name(Type=True, x=True):  # 获得名字统一接口
    global Form_List, Form_BOX, X_OUT
    if Type:
        try:
            return Form_List[Form_BOX.curselection()[0]]
        except:
            try:
                return Form_List[0]
            except:
                return None
    else:
        try:
            if x:
                return X_OUT.get()
            else:
                return Y_OUT.get()
        except:
            return None


def Update_BOX():
    global top, Form_BOX, Form_List
    Form_List = list(ML.get_Form().keys())
    Form_BOX.delete(0, tkinter.END)
    Form_BOX.insert(tkinter.END, *Form_List)

def Creat_TextSheet(data, name):
    global bg
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    text = ScrolledText(new_top, font=('黑体', 13), height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert('0.0', data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)

if __name__ == '__main__':
    Main()