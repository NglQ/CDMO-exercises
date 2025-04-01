import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

from z3 import *
import itertools

def plot_result(rects, W,H):
    w = W

    fig1 = plt.figure(figsize=(5, 5))
    ax1 = fig1.add_subplot(111, aspect='equal')
    for i in range(len(rects)):
        ax1.add_patch(patches.Rectangle((rects[i][2], rects[i][3]), rects[i][0], rects[i][1], edgecolor='black', facecolor=random.choice(['r', 'g', 'y','b'])))

    plt.xticks(range(W+1))
    plt.yticks(range(max([rects[i][3]+rects[i][1] for i in range(len(rects))])+1))
    #plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.show()


def return_coods(m,l,px,py):
  x_r =[]
  y_r=[]
  for r in range(l):
    x_r.append([m.eval(x) for x in px[r]].index(True))

  for r in range(l):
    y_r.append([m.eval(x) for x in py[r]].index(True))

  return list(zip(x_r,y_r))


def optimize(s,rects,px,py,under,left,W,H):
  #implict constraint: a rectangle can't be both right and left wrt another
  #same holds for under and over

  for (ri,rj) in itertools.combinations(range(len(rects)),2):
    s.add(Or(
        Not(left[ri][rj]),
        Not(left[rj][ri])
    ))
    s.add(Or(
        Not(under[ri][rj]),
        Not(under[rj][ri])
    ))


  #limit the dommain of the biggest rectangle, thus avoiding most symm options

  bigger_r = max(rects, key=lambda p:p[0]*p[1])
  ri = rects.index(bigger_r)

  limit_x = math.floor((W-bigger_r[0])/2)
  for x in range(limit_x):
    s.add(Not(px[ri][x]))
  for r in range(len(rects)):
    if r!= ri and rects[r][0] > limit_x+1:
      s.add(Not(left[ri][r]))

  limit_y = math.floor((H-bigger_r[1])/2)
  for y in range(limit_y):
    s.add(Not(py[ri][y]))
  for r in range(len(rects)):
    if r!= ri and rects[r][1] > limit_y+1:
      s.add(Not(under[ri][r]))

  #avoid combinations of rectangles that would go out of borders
  for (ri,rj) in itertools.combinations(range(len(rects)),2):
    if (rects[ri][0] + rects[rj][0] > W):
      s.add(Not(left[ri][rj]))
      s.add(Not(left[rj][ri]))

    if (rects[ri][1] + rects[rj][1] > H):
      s.add(Not(under[ri][rj]))
      s.add(Not(under[rj][ri]))

  #fix positions for same size rectangles
  for (ri,rj) in itertools.combinations(range(len(rects)),2):
    if (rects[ri] == rects[rj]):
      s.add(Not(left[rj][ri]))
      s.add(Or(Not(under[rj][ri]),left[ri][rj]))

  return s