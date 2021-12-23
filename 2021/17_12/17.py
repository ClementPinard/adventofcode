from tqdm import trange

(xmin, xmax), (ymin, ymax) = [[230,283],[-107,-57]]
#(xmin, xmax), (ymin, ymax) = [[20,30],[-10,-5]]

def max_height(yv):
    return int(yv*(yv+1)/2)

def inside(xv, yv):
    y_step = yv
    x_step = xv
    y=0
    x=0
    while (y + y_step >= ymin) and (x + x_step <= xmax):
        y += y_step
        y_step -=1
        x += x_step
        if x_step > 0:
            x_step -= 1
        #print(y , x)
    if y>= ymin and x <= xmax and y<= ymax and x>=xmin:
        return True
    else:
        return False

s = 0
for xv in range(xmax + 1):
    for yv in range(ymin, -ymin):
        success = inside(xv, yv)
        if success: 
            s += 1
            print(f"{xv}, {yv}")
        
print(s)