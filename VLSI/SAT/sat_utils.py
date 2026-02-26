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
  # TODO:
  #   1) implict constraint: a rectangle can't be both right and left wrt another
  #   2) same holds for under and over
  #   3) limit the dommain of the biggest rectangle, thus avoiding most symm options
  #   4) avoid combinations of rectangles that would go out of borders
  #   5) fix positions for same size rectangles


  return s
