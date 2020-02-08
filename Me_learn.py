import tkinter
from tkinter.filedialog import askopenfilename,asksaveasfilename
import tkinter.messagebox
import Learn
import webbrowser
import os
from tkinter.scrolledtext import ScrolledText
import chardet

#数据清洗
Clean_Text='''#输入你的数据清洗执行代码

Done_Row=[] #输入操作的行号
Done_Column=[] #输入操作的列号
axis=True #True-操作行，False-操作列
name='' #方法代号

def check(data,row,column,get,R,C): #检查方法
    return True

def done(data,row,column,get,R,C): #应用修正方法
    return DEL
'''

Clean_Help='''
使用Python代码进行数据清洗
1)代码结构
    Done_Row=[] 代码用来检测的数据的列号
    Done_Column=[] 代码用来检测的数据的行号
        不在以上指定范围内的数据将不会被检测，若为空则整个表格检测
    axis 执行删除方法时删除行或者列
    name 方法代号
    
    check 检查方法
        输入:当前的值(输入的是一个值而不是一行(列)或整个列表)
        输入:row和column当前值来自的行号(row)和列号(column)
        输入:get当前检查的所有数据:类型是表格
        输入:R和C当前值所来自的行和列的所有数据:类型是一维表格
        
        输出:输出布尔为True代表该值可以使用，输出布尔为假表示该值不可使用
        
    done 不可使用的数值改造方法
        输入:内容同上
        输出:改造值或者DEL
            DEL:代表删除改值所在的行(axis = True)或列(axis = False)
2)扩展
    默认:pd-pandas，re-re[正则表达式]，Sheet-包含所有表格，用Sheet['name']访问名字为name的表格(注意引号别漏了)
    支持:可以使用import导入语句，支持python语法
'''

Args_Help='''
输入python变量赋值代码:渲染设置
title #设置标题:str
vice_title #设置副标题:str

show_Legend #是否显示图例:bool

show_Visual_mapping #是否使用视觉映射:bool
is_color_Visual_mapping #是否为颜色视觉映射:bool[否则为大小视觉映射]
min_Visual_mapping #映射的最小值
max_Visual_mapping #映射的最大值

......(我太懒了,设置太多不想写了)
'''

def DTYPE():
    global Dtype_Column, Dtype_Input, Dtype_Wrong, Dtype_Func,ML
    type_ = bool(Dtype_Func.get())
    name = get_Name()
    column_list = Dtype_Column.get().split(',')
    if column_list == ['']:column_list = []
    dtype = Dtype_Input.get()
    wrong = Dtype_Wrong.get()
    if wrong != 'ignore':wrong = 'coerce'
    if type_:#软转换
        ML.Reasonable_Type(name,column_list,dtype,wrong)
    else:
        ML.as_Type(name,column_list,dtype,wrong)
    Updat_BOX()

def Import_c():#导入绘制方法
    global Done_Func
    Dic = askopenfilename(title='打开Python脚本',filetypes=[("Python", ".py"),("TXT", ".txt")])
    with open(Dic) as f:
        get = f.read()
        Render_ToHTML(ML.Import_c(get), '自定义图')

def get_ARGS():#获取画图的args
    global Args_Input
    return Args_Input.get('0.0',tkinter.END)

def Draw():
    global R_Dic,R_BOX
    Dic = asksaveasfilename(title='选择渲染保存地址',filetypes=[("HTML", ".html")]) + '.html'
    if Dic == '.html':return False
    webbrowser.open(ML.Draw_Page(get_ARGS(),Dic))
    Update_R_BOX()

def Draw_One():
    global R_Dic, R_BOX
    Dic = asksaveasfilename(title='选择渲染保存地址', filetypes=[("HTML", ".html")]) + '.html'
    if Dic == '.html': return False
    list(R_Dic.values())[R_BOX.curselection()[0]].render(Dic)
    webbrowser.open(Dic)
    Update_R_BOX()

def Del_R_BOX():
    global R_Dic,R_BOX,ML
    key = list(R_Dic.keys())[R_BOX.curselection()[0]]
    ML.Delete_RDic(key)
    Update_R_BOX()

def Update_R_BOX():
    global R_Dic,R_BOX,ML
    R_Dic = ML.retunr_RDic()
    R_BOX.delete(0, tkinter.END)
    R_BOX.insert(tkinter.END, *R_Dic.keys())

def Render_ToHTML(c,name):
    global R_Dic,Draw_asWell
    if bool(Draw_asWell.get()):
        c.render(f'{PATH}\\{name}.html')
    Update_R_BOX()

def to_Gauge():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Gauge(name,get_ARGS()),'仪表图')

def to_Liquid():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Liquid(name,get_ARGS()),'水球图')

def to_Line3D():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Line3D(name,get_ARGS()),'3D折线图')

def to_Scatter3D():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Scatter3D(name,get_ARGS()),'3D散点图')

def to_Bar3d():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Bar3d(name,get_ARGS()),'3D柱状图')

def to_WordCloud():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_WordCloud(name,get_ARGS()),'词云图')

def to_Radar():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Radar(name,get_ARGS()),'雷达图')

def to_Polar():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Polar(name,get_ARGS()),'极坐标图')

def to_Pie():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Pie(name,get_ARGS()),'饼图')

def to_Parallel():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Parallel(name,get_ARGS()),'多轴图')

def to_Graph():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Graph(name,get_ARGS()),'关系图')

def to_Funnel():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Funnel(name,get_ARGS()),'漏斗图')

def to_HeatMap():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_HeatMap(name,get_ARGS()),'热力图')

def to_Boxpolt():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Boxpolt(name,get_ARGS()),'箱形图')

def to_Pictorialbar():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Pictorialbar(name,get_ARGS()),'象形柱状图')

def to_Scatter():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Scatter(name,get_ARGS()),'散点图')

def to_Line():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Line(name,get_ARGS()),'折线图')

def to_Bar():
    global ML
    name = get_Name()
    Render_ToHTML(ML.to_Bar(name,get_ARGS()),'柱状图')

def Show_Help():
    tkinter.messagebox.showinfo('帮助字典',Clean_Help)

def Open_Python():
    global Done_Func
    Dic = askopenfilename(title='打开Python脚本',filetypes=[("Python", ".py"),("TXT", ".txt")])
    with open(Dic) as f:
        get = f.read()
        Done_Func.delete('0.0', tkinter.END)
        Done_Func.insert('0.0', get)

def get_InsertClean_Text():
    global Done_Func,Clean_Text
    Done_Func.delete('0.0',tkinter.END)
    Done_Func.insert('0.0',Clean_Text)

def get_CleanEXP():
    global ML,Clean_List,Done_CleanBox,Done_Func
    name = Clean_List[Done_CleanBox.curselection()[0]]
    get = ML.Return_CleanExp(name)
    Done_Func.delete('0.0',tkinter.END)
    Done_Func.insert('0.0',get)

def Tra_Clean():
    global ML
    ML.Tra_Clean()
    Updat_BOX()

def Done_Clean():
    global ML
    name = get_Name()
    Data = ML.Done_CleanFunc(name)
    title = f'CoTan机器学习 表格:{name}.数据清洗'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Del_Clean():
    global ML,Clean_List,Done_CleanBox
    name = Clean_List[Done_CleanBox.curselection()[0]]
    ML.Delete_CleanFunc(name)
    Update_Clean()

def Update_Clean():
    global ML,Done_CleanBox,Clean_List
    Clean_List = ML.Return_CleanFunc()
    Done_CleanBox.delete(0, tkinter.END)
    Done_CleanBox.insert(tkinter.END, *Clean_List)

def Add_Clean():
    global ML,Done_CleanBox,Done_Func
    Exp = Done_Func.get('0.0',tkinter.END)
    print(Exp)
    ML.Add_CleanFunc(Exp)
    Update_Clean()

def Done_NaN():
    global Drop_Column
    name = get_Name()
    Data = ML.Dropna(name,True)
    title = f'CoTan机器学习 表格:{name}.NaN'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def is_Na():
    global Bool_E
    name = get_Name()
    Data = ML.is_Na(name)
    title = f'CoTan机器学习 表格:{name}.NaN'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Make_BoolSheet():
    global Bool_E
    Bool_Exp = Bool_E.get()
    name = get_Name()
    Data = ML.Done_Bool(name,Bool_Exp,True)
    print(Data)
    title = f'CoTan机器学习 表格:{name} 布尔化'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Del_Data():
    global Slice_new, Column_clist, Row_clist
    Column = Column_clist[0].get().replace(' ','').split(',')
    Row = Row_clist[0].get().replace(' ', '').split(',')
    new = bool(Slice_new.get())
    name = get_Name()
    try:
        Data = ML.Delete(name,Column,Row,new)
    except:
        Data = 'None 你的操作不被允许'
    title = f'CoTan机器学习 表格:{name}'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def __get_clist(n,t=str):
    a = []
    for i in n:
        b = i.get().replace(' ','')
        if b == '':a.append(None)
        else:
            try:a.append(t(b))
            except:a.append(None)
    if a[0] != None and a[1] == None:
        a[1] = a[0]+1
        a[2] = None
    return a

def Slice_Data():
    global Slice_new, Column_Type, Row_Type, Column_clist, Row_clist
    CT = Column_Type.get()
    U = True
    if CT == 0:#输入的列号
        Column = slice(*__get_clist(Column_clist,int))
    elif CT == 1:
        U = False
        Column = slice(*__get_clist(Column_clist, str))
    else:
        get = Column_clist[0].get().replace(' ','').split(',')
        Column = []
        for i in get:
            try:Column.append(int(i))
            except:pass

    RT = Row_Type.get()
    if RT == 0:  # 输入的列号
        Row = slice(*__get_clist(Row_clist, int))
    elif RT == 1:
        Row = slice(*__get_clist(Row_clist, str))
    else:
        get = Row_clist[0].get().replace(' ', '').split(',')
        Row = []
        for i in get:
            try:
                Row.append(int(i))
            except:
                pass
    new = bool(Slice_new.get())
    name = get_Name()
    try:
        Data = ML.get_Clice(name,Column,Row,U,new)
    except:
        Data = 'None 你的操作不被允许'
    title = f'CoTan机器学习 表格:{name}'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Stored_Value():
    global ML,Stored_List
    name = get_Name()
    new = bool(Ascending_New.get())
    Data = ML.Stored_Valuse(name, Stored_List,new)
    title = f'CoTan机器学习 表格:{name}.Stored'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Tra_Stored_Value():
    global Stored_List, Stored_BOX
    Stored_List = []
    Update_Stored()

def Delete_Stored_Value():
    global Stored_List,Stored_BOX,Ascending_Type
    del Stored_List[Stored_BOX.curselection()[0]]
    Update_Stored()

def add_Stored_Value():#按基准列排行
    global ML,Stored_List,Sort_By,Ascending_Type
    try:
        a = not bool(Ascending_Type.get())
        value = int(Sort_By.get())
        Stored_List.append((value,a))
    except:pass
    Update_Stored()

def Update_Stored():
    global Stored_List,Stored_BOX
    re = []
    d = {True:'正序',False:'倒叙'}
    for i in Stored_List:
        re.append(f"列号:{i[0]},排序方式{d[i[1]]}")
    Stored_BOX.delete(0,tkinter.END)
    Stored_BOX.insert(tkinter.END,*re)

def Stored_Column():#行
    global ML
    name = get_Name()
    a = not bool(Ascending_Type.get())
    new = bool(Ascending_New.get())
    Data = ML.Sorted(name,False,new,a)
    title = f'CoTan机器学习 表格:{name}.Stored by Column'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Stored_Row():#行
    global ML
    name = get_Name()
    new = bool(Ascending_New.get())
    a = not bool(Ascending_Type.get())
    Data = ML.Sorted(name,True,new,a)
    title = f'CoTan机器学习 表格:{name}.Stored by Row'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def T():
    global ML
    name = get_Name()
    new = bool(Ascending_New.get())
    Data = ML.T(name,new)
    title = f'CoTan机器学习 表格:{name}.T'
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Show_Des():
    global PATH,top
    if not tkinter.messagebox.askokcancel('提示', f'是否统计数据，大量的数据需要耗费一定的时间(确定后，系统会在后台统计)'):return False
    Dic = f'{PATH}/$Show_Des_Sheet.html'
    try:
        name = get_Name()
        if name == None:raise Exception
        ML.to_Report(name,Dic)
        webbrowser.open(Dic)
    except:
        pass

def Show_describe():
    global ML,Des_Bool
    Des = bool(Des_Bool.get())
    name = get_Name()
    title = f'CoTan机器学习 表格:{name}_describe'
    Data = str(ML.Describe(name,Des))
    Creat_TextSheet(Data, title)
    Updat_BOX()

def Write_Sheet():
    global ML,top
    name = get_Name()
    title = f'CoTan机器学习 表格:{name}'
    Data = str(ML.get_Sheet(name))
    Creat_TextSheet(Data,title)

def Creat_TextSheet(data,name):
    global bg,ft1
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')#设置所在位置
    text = ScrolledText(new_top,font=ft1,height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert('0.0',data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)

def get_Column():#列名(横行竖列，列名是上面的)
    global ML
    name = get_Name()
    Updat_IndexBOX(ML.get_Column(name))

def get_Index():#行名(横行竖列，行名左)
    global ML
    name = get_Name()
    Updat_IndexBOX(ML.get_Index(name))

def Updat_IndexBOX(get_Index):
    global top,Index_BOX
    Index_BOX.delete(0,tkinter.END)
    Index_BOX.insert(tkinter.END, *get_Index)

def Show():
    global PATH,to_HTML_Type
    Dic = f'{PATH}/$Show_Sheet.html'
    try:
        name = get_Name()
        if name == None:raise Exception
        ML.to_Html(name,Dic,to_HTML_Type.get())
        webbrowser.open(Dic)
    except:
        raise

def Add_CSV():
    global top,Seq_Input,Code_Input,str_must,Index_must
    Dic = askopenfilename(title='选择载入的CSV',filetypes=[("CSV", ".csv")])
    Seq = Seq_Input.get()
    Codeing = Code_Input.get()
    str_ = bool(str_must.get())
    Index = bool(Index_must.get())
    if Codeing == '':
        with open(Dic, 'rb') as f:
            Codeing = chardet.detect(f.read())['encoding']
            print(Codeing)
    if Seq == '':Seq = ','
    ML.Add_CSV(Dic,'',Seq,Codeing,str_,Index)
    Updat_BOX()

def Add_Python():
    global top,Seq_Input,Code_Input,str_must,Index_must
    Dic = askopenfilename(title='选择载入的py',filetypes=[("Python", ".py"),("Txt", ".txt")])
    with open(Dic,'r') as f:
        ML.Add_Python(f.read(),'')
    Updat_BOX()

def Add_Html():
    global top,Seq_Input,Code_Input,str_must,Index_must
    Dic = askopenfilename(title='选择载入的Html',filetypes=[("CSV", ".csv")])
    Codeing = Code_Input.get()
    str_ = bool(str_must.get())
    Index = bool(Index_must.get())
    if Codeing == '':
        with open(Dic, 'rb') as f:
            Codeing = chardet.detect(f.read())['encoding']
            print(Codeing)
    ML.Add_Html(Dic,'',Codeing,str_,Index)
    Updat_BOX()

def get_Name():#获得名字统一接口
    global Form_List
    try:
        return Form_List[Form_BOX.curselection()[0]]
    except:
        try:
            return Form_List[0]
        except:
            return None

def Updat_BOX():
    global top,Form_BOX,Form_List
    Form_List = ML.get_FormList()
    Form_BOX.delete(0,tkinter.END)
    Form_BOX.insert(tkinter.END, *Form_List)

def Machine_learning():
    global top,ML,Form_List,PATH,bg,ft1,Stored_List,Clean_List,R_Dic
    R_Dic = {}#保存了画图的List
    PATH = os.getcwd()
    Form_List = []
    ML = Learn.Form()
    top = tkinter.Tk()
    bg = '#FFFAFA'#主颜色
    bbg = '#FFFAFA'#按钮颜色
    fg = '#000000'#文字颜色
    top["bg"] = bg
    FONT = ('黑体', 11)#设置字体
    ft1 = ('黑体',13)
    top.title('CoTan机器学习')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')#设置所在位置
    width_B = 13#标准宽度
    height_B=2
    a_y = 0
    a_x = 0
    Stored_List = []
    Clean_List = []

    tkinter.Button(top, bg=bbg, fg=fg, text='导入CSV',command=Add_CSV, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入Py',command=Add_Python, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入HTML',command=Add_Html, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除表格', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看表格',command=Show, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空表格', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    global Form_BOX,Index_BOX,Column_BOX,to_HTML_Type,Seq_Input,Code_Input,str_must,Index_must
    a_y += 1
    to_HTML_Type = tkinter.IntVar()#正，负，0
    lable = ['选项卡型','可移动型','自适应型']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i], variable=to_HTML_Type,
                            value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    str_must = tkinter.IntVar()
    Index_must = tkinter.IntVar()
    a_y += 1
    tkinter.Label(top, text='编码方式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Code_Input = tkinter.Entry(top, width=width_B)
    Code_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    buttom = tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='字符串类型',
                        variable=str_must)
    buttom.select()
    buttom.grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='CSV分隔符:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Seq_Input = tkinter.Entry(top, width=width_B)
    Seq_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='重置列名',
                        variable=Index_must).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    Form_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*5)  # 显示符号
    Form_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5,sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='查看行名',command=get_Index, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看列名',command=get_Column, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='显示表格',command=Write_Sheet, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    global Max_Row,Max_Column
    a_y += 1
    tkinter.Label(top, text='最大显示行数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Max_Row = tkinter.Entry(top, width=width_B * 2)
    Max_Row.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='最大显示列数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Max_Column = tkinter.Entry(top, width=width_B * 2)
    Max_Column.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    #Row与Column Row是横行，tkinter布局中Row变大，表示所在行数变大，向下移动如：
    # 1，2，3，4，5，6
    # 7，8，9，a，b，c
    # 其中数字1-6是第一行，1-c是第二行，第二行在第一行下面，row变大向下移动（Row是横向行而不是横向移动） to 搞不清楚横行竖列的人

    a_y += 1
    Index_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*3)  # 显示符号
    Index_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3,sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global Des_Bool
    a_y += 3
    tkinter.Button(top, bg=bbg, fg=fg, text='查看数据分析',command=Show_Des, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='简单数据统计',command=Show_describe, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    Des_Bool = tkinter.IntVar()#是否启用
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成统计表格',
                        variable=Des_Bool).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='【排序操作】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(column=a_x,
                                                                                               columnspan=3,row=a_y)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='表格转置', command=T, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='按行名排序', command=Stored_Row, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='按列名排序', command=Stored_Column, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    global Sort_By,Ascending_Type,Ascending_New,Stored_BOX
    a_y += 1
    tkinter.Label(top, text='基准列(列号):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Sort_By = tkinter.Entry(top, width=width_B+2)
    Sort_By.grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='按数据排序', command=Stored_Value, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    Ascending_Type = tkinter.IntVar()
    Ascending_New = tkinter.IntVar()
    lable = ['正序排列','倒序排列']#复选框
    for i in range(2):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i], variable=Ascending_Type, value=i).\
            grid(column=a_x+i, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成新表格',
                        variable=Ascending_New).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    Stored_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*3)  # 显示符号
    Stored_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3,sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 3
    tkinter.Button(top, bg=bbg, fg=fg, text='添加基准', command=add_Stored_Value, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除基准', command=Delete_Stored_Value, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空基准', command=Tra_Stored_Value, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x,row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【数据清洗】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(column=a_x,
                                                                                               columnspan=3,row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明

    global Slice_new,Column_Type,Row_Type,Column_clist,Row_clist
    Column_clist = []
    Row_clist = []
    label = ['启始(列号):','终止(列):','间隔(列):']
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text=label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
        Column_clist.append(tkinter.Entry(top, width=width_B * 2))
        Column_clist[-1].grid(column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.W+tkinter.E)

    label = ['启始(行号):', '终止(行):', '间隔(行):']
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text=label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
        Row_clist.append(tkinter.Entry(top, width=width_B * 2))
        Row_clist[-1].grid(column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.W+tkinter.E)

    a_y += 1
    Column_Type = tkinter.IntVar()
    lable = ['根据列号','根据列名','输入列号']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i], variable=Column_Type, value=i).\
            grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    Row_Type = tkinter.IntVar()
    lable = ['根据行号','根据行名','输入行号']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i], variable=Row_Type, value=i).\
            grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    Slice_new = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='切片选定', command=Slice_Data, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除选定', command=Del_Data, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成新表格',
                        variable=Slice_new).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    global Bool_E,Drop_Column
    a_y += 1
    tkinter.Label(top, text='布尔逻辑:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明
    Bool_E = tkinter.Entry(top, width=width_B*2)
    Bool_E.grid(column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.W+tkinter.E)

    a_y += 1
    tkinter.Label(top, text='操作的列号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明
    Drop_Column = tkinter.Entry(top, width=width_B*2)
    Drop_Column.grid(column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.W+tkinter.E)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成布尔表格', command=Make_BoolSheet, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看空值', command=is_Na, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='清洗空值(按行)', command=Done_NaN, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='添加执行方法', command=Add_Clean, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除执行方法', command=Del_Clean, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='执行数据清洗', command=Done_Clean, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    global Done_CleanBox,Done_Func
    a_y += 1
    Done_CleanBox = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    Done_CleanBox.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    tkinter.Button(top, bg=bbg, fg=fg, text='查看词典', command=Show_Help, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复显示', command=get_InsertClean_Text, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='执行数据清洗', command=Done_Clean, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    Done_Func = tkinter.Text(top,width=width_B*3,height=height_B*7)
    Done_Func.grid(column=a_x, row=a_y,columnspan=3,rowspan=7, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)
    Done_Func.insert('0.0',Clean_Text)

    a_y += 7
    tkinter.Button(top, bg=bbg, fg=fg, text='清空执行方法', command=Tra_Clean, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看执行方法', command=get_CleanEXP, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入执行方法', command=Open_Python, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x,row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【数据画图】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(column=a_x,
                                                                                               columnspan=3,row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成柱状图', command=to_Bar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D柱状图', command=to_Bar3d, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成折线图', command=to_Line, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D折线图', command=to_Line3D, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成象形柱状图', command=to_Pictorialbar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成散点图', command=to_Scatter, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D散点图', command=to_Scatter3D, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成箱形图', command=to_Boxpolt, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成漏斗图', command=to_Funnel, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成关系图', command=to_Graph, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成饼图', command=to_Pie, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成多轴图', command=to_Parallel, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成极坐标图', command=to_Polar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成雷达图', command=to_Radar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成词云', command=to_WordCloud, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成热力图', command=to_HeatMap, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成水球图', command=to_Liquid, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成仪表图', command=to_Gauge, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='渲染HTML', command=Draw, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='单独渲染HTML', command=Draw_One, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除渲染', command=Del_R_BOX, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    a_y += 1
    global R_BOX,Args_Input
    R_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 3)
    R_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 3
    global Draw_asWell
    Draw_asWell = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='清空渲染', command=Draw, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入渲染', command=Draw, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='马上渲染',
                        variable=Draw_asWell).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    a_y += 1
    Args_Input = tkinter.Text(top,width=width_B*3,height=height_B*4)
    Args_Input.grid(column=a_x, row=a_y,columnspan=3,rowspan=6, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    a_y += 6
    tkinter.Button(top, bg=bbg, fg=fg, text='查看词典', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复显示', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y,columnspan = 2, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)

    global Dtype_Column,Dtype_Input,Dtype_Wrong,Dtype_Func
    a_y += 1
    tkinter.Label(top, text='【数据类型管理】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(column=a_x,
                                                                                               columnspan=3,row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Label(top, text='修改(列号):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Dtype_Column = tkinter.Entry(top, width=width_B * 2)
    Dtype_Column.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='数据类型:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Dtype_Input = tkinter.Entry(top, width=width_B * 2)
    Dtype_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='错误值:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Dtype_Wrong = tkinter.Entry(top, width=width_B * 2)
    Dtype_Wrong.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='执行转换',command=DTYPE, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)
    Dtype_Func = tkinter.IntVar()#正，负，0
    lable = ['硬转换','软转换']#复选框
    for i in range(2):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i],
                            variable=Dtype_Func, value=i).grid(column=a_x+1+i, row=a_y, sticky=tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x,row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【行名与列名】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(column=a_x,
                                                                                               columnspan=3,row=a_y, sticky=tkinter.E + tkinter.W + tkinter.W+tkinter.S + tkinter.N)  # 设置说明

    global replace_Dic,Repalce_RC,replace_iloc,Date_Input,RC_Type
    a_y += 1
    Repalce_RC = tkinter.IntVar()
    lable = ['(列数据)调整行名','(行数据)调整列名']#复选框
    for i in range(2):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i],
                            variable=Repalce_RC, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='植入行(列)号',command=num_withName, font=FONT, width=width_B,height=height_B).\
        grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    RC_Type = []
    lable = ['保留原值','保留新值']#复选框
    for i in range(2):
        RC_Type.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i],
                            variable=RC_Type[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='统一行号',command=num_toName, font=FONT, width=width_B,height=height_B).\
        grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='替换字典:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    replace_Dic = tkinter.Entry(top, width=width_B * 2)
    replace_Dic.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='替换列(行):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    replace_iloc = tkinter.Entry(top, width=width_B * 2)
    replace_iloc.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='执行替换已有列(行)操作',command=Change_Index, font=FONT, width=width_B*2, height=height_B). \
        grid(column=a_x,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='执行替换操作',command=Replace_Index, font=FONT, width=width_B,height=height_B).\
        grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    label = ['起点','终点','间隔']
    Date_Input = []
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text='时间序列'+label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
        Date_Input.append(tkinter.Entry(top, width=width_B * 2))
        Date_Input[-1].grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    global Date_Type
    a_y += 1
    Date_Type = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='刷入Date序列',command=Date_Index, font=FONT, width=width_B,height=height_B).\
        grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='刷入Time序列',command=Time_index, font=FONT, width=width_B, height=height_B). \
        grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='使用间隔',
                        variable=Date_Type).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    top.mainloop()

#出现在此下面的函数应转移到上方方便管理！......

def Replace_Index():
    global replace_Dic, Repalce_RC,ML
    name = get_Name()
    Dic = eval(replace_Dic.get())
    is_Column = bool(Repalce_RC.get()) #操作行-False，操作列-True
    save = bool(RC_Type[0].get())

    ML.Replace_Index(name,is_Column,Dic,save)
    Updat_BOX()

def Change_Index():
    global Repalce_RC, replace_iloc, RC_Type,ML
    name = get_Name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    iloc = int(replace_iloc.get()) # 替换的列号(行号)
    save = bool(RC_Type[0].get())
    drop = not bool(RC_Type[1].get())

    ML.Change_Index(name,is_Column,iloc,save,drop)
    Updat_BOX()

def num_toName():
    global Repalce_RC, replace_iloc, RC_Type,ML
    name = get_Name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    ML.num_toName(name,is_Column,save)
    Updat_BOX()

def num_withName():
    global Repalce_RC,RC_Type,ML
    name = get_Name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    ML.num_withName(name,is_Column,save)
    Updat_BOX()

def DateTime_Index(is_Date=True):
    global Repalce_RC, RC_Type,ML,Date_Input,Date_Type
    name = get_Name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    k = ['start','end','freq']
    Init = {}
    for i in range(len(Date_Input)):
        Input = Date_Input[i].get()
        if Input == '':continue
        Init[k[i]] = Input
    if len(Init) == 3:
        if bool(Date_Type.get()):#使用间隔
            del Init['end']
        else:
            del Init['freq']
    if is_Date:
        ML.Date_Index(name,is_Column,save,**Init)
    else:
        ML.Time_Index(name, is_Column, save, **Init)
    Updat_BOX()

def Date_Index():
    DateTime_Index(True)

def Time_index():
    DateTime_Index(False)

if __name__ == '__main__':
    Machine_learning()