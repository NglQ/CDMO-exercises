from z3 import *
import itertools


def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in itertools.combinations(bool_vars, 2)]

def base_model_order(s,rects,px,py,under,left,W,H):
  #non overlapping condition
  for (i,j) in itertools.combinations(range(len(rects)),2):
    s.add(Or(left[i][j],left[j][i],under[i][j],under[j][i]))

  #implicit domains
  for r in range(len(rects)):
    for xi in range(W-rects[r][0],W):
      s.add(px[r][xi])
    for yi in range(H-rects[r][1],H):
      s.add(py[r][yi])
  #order encoding
  for r in range(len(rects)):
    for e in range(W-1):
      s.add(Or(Not(px[r][e]),px[r][e+1]))
    for f in range(H-1):
      s.add(Or(Not(py[r][f]),py[r][f+1]))



  #meaning for left and under
  for ri in range(len(rects)):
    for rj in range(len(rects)):
      if ri != rj :
        #print((ri,rj))
        s.add(Or(
            Not(left[ri][rj]),
            Not(px[rj][rects[ri][0]-1])
        )) # left(ri,rj) -> xj > wi, lower bound for xj
        for e in range(0,W-rects[ri][0]):
          s.add(Or(
              Not(left[ri][rj]),
              px[ri][e],
              Not(px[rj][e+rects[ri][0]])
          )) #for any e: left(ri,rj) -> (xi <e v ! xj<e+wi)

        s.add(Or(
            Not(under[ri][rj]),
            Not(py[rj][rects[ri][1]-1])
        )) #under(ri,rj)-> yj > hi, lower bound for yj

        for f in range(0,H-rects[ri][1]):
          s.add(Or(
              Not(under[ri][rj]),
              py[ri][f],
              Not(py[rj][f+rects[ri][1]])
        )) #for any f, under(ri,rj) -> (yj <= f+hi ->yi <= f)
  return s
