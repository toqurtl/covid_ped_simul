import os

idx_list = [ 22, 32, 64, 15, 24, 25, 29, 65,67,69,71,74,76,78,79,96,97,105,107,109,110,111,114,117,118,121,122,124,126,127,131,136,137,140,141,142,143,144,147 ]

# for idx in idx_list:
#     os.system('python app_simulate.py '+str(idx)+' 0')

# for idx in idx_list:
#     os.system('python app_simulate.py '+str(idx)+' 1')


for idx in idx_list:
    print(idx)
    os.system('python app_validate.py '+str(idx)+' 0')

for idx in idx_list:
    print(idx)
    os.system('python app_validate.py '+str(idx)+' 1')