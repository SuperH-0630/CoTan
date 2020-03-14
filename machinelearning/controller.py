from machinelearning.template import MachineLearnerAdd, MachineLearnerScore, LearnerActions


class MachineLearner(MachineLearnerAdd, MachineLearnerScore, LearnerActions):  # 数据处理者

    def return_learner(self):
        return self.learner.copy()

    def del_leaner(self, leaner):
        del self.learner[leaner]
        del self.data_type[leaner]
