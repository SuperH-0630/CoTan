from funcsystem.template import *


class SheetFunc(SheetMemory, SheetComputing, SheetDataPacket, SheetProperty, SheetBestValue):

    def save_csv(self, file_dir):
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        try:
            self.dataframe.to_csv(file_dir)
        except BaseException:
            return False
        else:
            return True

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


class ExpFunc(ExpMemory, ExpComputing, ExpCheck, ExpDataPacket, ExpProperty, ExpBestValue):
    def return_son(self):
        return self.son_list

    def save_csv(self, file_dir):
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        try:
            self.dataframe.to_csv(file_dir)
        except BaseException:
            return False
        else:
            return True

    def return_list(self):  # 导出列表
        if not self.have_data_packet:
            self.data_packet()
        # 最值和极值点设计
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
