from algebraicfactory.template import AlgebraVisualization, AlgebraPolynomialSplit, AlgebraPolynomialMerge, \
    Fractional, Trig, AlgebraMul, General, AlgebraComplex, AlgebraSpecialFunc, Simultaneous, Sloving, Digitization, \
    AlgebraSimplify, Rewrite, AlgebraPlot


class AlgebraPolynomial(AlgebraVisualization, AlgebraPolynomialSplit, AlgebraPolynomialMerge,
                        Fractional, Trig, AlgebraMul, General, AlgebraComplex, AlgebraSpecialFunc, Simultaneous,
                        Sloving, Digitization, AlgebraSimplify, Rewrite, AlgebraPlot):
    def __call__(self):  # 返回符号信息
        alg_view = []
        alg = []
        for name in self.algebra_dict:
            alg.append(name)
            alg_view.append(f"{name} --> {self.algebra_dict[name]}")
        value = []
        value_view = []
        for name in self.symbol_describe:
            value.append(name)
            value_view.append(f"符号:{name} --> {self.symbol_describe[name]}")
        return (value_view, value), (alg_view, alg)

    def get_expression_from_name(self, name):
        alg = self.get_expression(name)
        return self.formula_export(alg)
