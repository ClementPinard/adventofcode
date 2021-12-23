from collections import deque
from functools import reduce

with open("input.txt") as f:
    packets = f.read()
    
packets_list = "".join([f"{int(p, 16):>04b}" for p in packets if p!="\n"])
packets_queue = deque(packets_list)

def pop(packets, n=1, convert=True):
    number = ''.join(packets.popleft() for i in range(n))
    return int(number, 2) if convert else number

def get_data(packets):
    data = []
    while True:
        g_type = pop(packets, 1)
        data.append(pop(packets, 4, convert=False))
        if g_type == 0:
            break
    data = int(''.join(data), 2)
    return data
    
def parse(packets):
    p_version = pop(packets, 3)
    p_type = pop(packets, 3)
    if p_type == 4:
        data = get_data(packets)
    else:
        l_type = pop(packets)
        if l_type == 0:
            length = pop(packets, 15)
            data=[]
            len_before = len(packets)
            while len_before - len(packets) < length:
                data.append(parse(packets))
        else:    
            n = pop(packets, 11)
            data = []
            for j in range(n):
                data.append(parse(packets))
        if p_type == 0:
            data = sum(data)
        elif p_type == 1:
            data = reduce(lambda x,y: x*y, data)
        elif p_type == 2:
            data = min(data)
        elif p_type == 3:
            data = max(data)
        elif p_type == 5:
            data = int(data[0] > data[1])
        elif p_type == 6:
            data = int(data[0] < data[1])
        elif p_type == 7:
            data = int(data[0] == data[1])
    return data

print(parse(packets_queue))