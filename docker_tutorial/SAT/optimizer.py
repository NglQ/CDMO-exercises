import time

from z3 import *

from SAT.sat_utils import plot_result, return_coods, optimize
from SAT.encodings import base_model_order
from SAT.sat_utils import optimize


def solve(rects,W,totarea,opt=False):
  start = time.time()
  solved= False
  Hmin = int(totarea/W)
  Hmax = int(2*max(max(rects, key=lambda p:p[0]*p[1])[1],totarea/W))+1
  ul = Hmax
  ll = Hmin
  H = ll
  while (ll < ul):
    if (time.time() - start > 300):
      print("out of time")
      return False, (300,300), (0,0,0)
    #print(f"Solving for H={H}")
    px = [[Bool(f"px{r+1}_{x}") for x in range(W)] for r in range(len(rects))]
    py = [[Bool(f"py{r+1}_{y}") for y in range(H)] for r in range(len(rects))]
    under = [[Bool(f"r{ri+1}_under_r{rj+1}") if ri != rj else 0 for rj in range(len(rects)) ] for ri in range(len(rects))]
    left = [[Bool(f"r{ri+1}_leftof_r{rj+1}")  if rj!=ri else 0 for rj in range(len(rects))] for ri in range(len(rects))]
    s = Solver()
    s.set("timeout", 300*1000)

    s = base_model_order(s,rects,px,py,under,left,W,H)
    if opt == True :
      s = optimize(s,rects,px,py,under,left,W,H)

    checking_from = time.time()
    if s.check() == z3.sat :
      ul = H
    else:
      ll = H+1
    H =  int((ll+ul)/2)
    checked_in = time.time() - checking_from
  m = s.model()
  end=time.time()
  elapsed = end-start
  return True, (elapsed,checked_in), (m,return_coods(m,len(rects),px,py),H)
