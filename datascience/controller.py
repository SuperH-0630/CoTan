from datascience.template import VisualLearner, Learner


class MachineLearner(VisualLearner, Learner):  # 数据处理者

    def add_learner(self, learner, parameters=""):
        get, args_tuple = self.learn_dict[learner]
        name = f"Le[{len(self.learner)}]{learner}"
        # 参数调节
        args_use = self.parsing(parameters)
        args = {}
        for i in args_tuple:
            args[i] = args_use[i]
        # 生成学习器
        self.learner[name] = get(**args)
        self.learner_type[name] = learner

    def return_learner(self):
        return self.learner.copy()

    def del_leaner(self, leaner):
        del self.learner[leaner]
        del self.learner_type[leaner]
