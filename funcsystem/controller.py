import tkinter.messagebox
import tkinter.filedialog

from funcsystem.template import SheetFuncBase, SheetProperty, SheetMemory, ExpFuncBase, ExpMemory, ExpComputing, \
    ExpCheck


class SheetFunc(SheetProperty, SheetMemory, SheetFuncBase):

    def save_csv(self):
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        if tkinter.messagebox.askokcancel("提示", f"是否确认导出函数:\n{str(self)}"):
            try:
                file_dir = (
                    tkinter.filedialog.asksaveasfilename(
                        title="选择导出位置", filetypes=[("CSV", ".csv")]
                    )
                    + ".csv"
                )
                if file_dir == ".csv":
                    raise Exception
                self.dataframe.to_csv(file_dir)
                return True
            except BaseException:
                pass
        return False

    def return_list(self):
        # 最值和极值点设计
        # if not self.HaveDone: self.Cul()  # 检查Cul的计算
        a = []
        for i in self.min_x:
            a.append(f"极值点：{i}>最小值{self.min_y}")
        for i in self.max_x:
            a.append(f"极值点：{i}>最大值{self.max_y}")
        return a + self.memory_answer + self.xy_sheet

    def get_plot_data(self):
        if not self.have_data_packet:
            self.data_packet()
        return (
            self.classification_x,
            self.classification_y,
            self.func_name,
            self.style,
        )


class ExpFunc(ExpMemory, ExpComputing, ExpCheck, ExpFuncBase):

    def return_son(self):
        return self.son_list

    def save_csv(self):
        if not self.have_data_packet:
            self.data_packet(float)
        if tkinter.messagebox.askokcancel("提示", f"是否确认导出函数:\n{str(self)}"):
            try:
                file_dir = (
                    tkinter.filedialog.asksaveasfilename(
                        title="选择导出位置", filetypes=[("CSV", ".csv")]
                    )
                    + ".csv"
                )
                if file_dir == ".csv":
                    raise Exception
                self.dataframe.to_csv(file_dir)
                return True
            except BaseException:
                pass
        return False

    def return_list(self):  # 导出列表
        if not self.have_data_packet:
            self.data_packet(float)
        # 最值和极值点设计
        a = []
        for i in self.min_x:
            a.append(f"极值点：{i}>最小值{self.min_y}")
        for i in self.max_x:
            a.append(f"极值点：{i}>最大值{self.max_y}")
        return a + self.memory_answer + self.xy_sheet

    def get_plot_data(self):
        if not self.have_data_packet:
            self.data_packet(float)
        return (
            self.classification_x,
            self.classification_y,
            self.func_name,
            self.style,
        )
