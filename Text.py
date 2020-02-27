# import numpy as np
#
# Dic = r'C:\Users\宋子桓\Desktop\CSV表格'
#
# x=np.linspace(0,1,1400)
# z=np.linspace(8,9,1400)
# y=7*np.sin(2*np.pi*20*x) + 5*np.sin(2*np.pi*40*z)+3*np.sin(2*np.pi*60*z)
#
# # o = np.vstack(x,z)
# np.savetxt(Dic + r"/sin_x.csv", y, delimiter=',')

# from scipy.fftpack import fft, ifft
# import numpy as np
# x = np.arange(5)
# a = fft(x)
# b = ifft(a)
# print(a)
# print(b)
# print(a.dtype)
# print(b.dtype)

import numpy as np

a = np.array([1,2,3,4,5])
b = np.array([1,2,3,4,5])
c = a + b * 1j
print(c)