flag_rev = '{FTCocip5_14m1n44x4_31y746_g41f_}611772'
flag = ''

for i in range(0, len(flag_rev), 8):
    chunk = flag_rev[i:i+8]
    rev_chunk = chunk[::-1]
    flag += rev_chunk

print(flag)

