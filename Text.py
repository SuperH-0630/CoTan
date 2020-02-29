# import subprocess
#
# a = subprocess.Popen('dir;dir',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
#                      cwd=r'C:\Users\宋子桓\Desktop\Git_Test')
# # print(a.stdout())
# a.wait()
# print(a.returncode)
# while True:
#     i = a.stdout.readline().decode('utf-8')
#     if i == '':break
#     print(i,end='')

a = '&&'
# b = ['1','2','3']
b = ['1']
print(a.join(b))