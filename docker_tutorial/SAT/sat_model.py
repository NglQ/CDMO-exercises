import os

from SAT.optimizer import solve
from SAT.sat_utils import plot_result

def sat_solver():

  os.makedirs('SAT/outputs', exist_ok=True)
  instances = os.listdir('SAT/instances')
  for i, filename in enumerate(instances):
    print(f"instance:{filename}")
    with open('SAT/instances/'+filename, "r") as file1:
      FileasList = file1.readlines()
    W=int(FileasList[0])
    N=int(FileasList[1])
    rects=[]
    results=[]
    totarea=0
    for n in range(2,2+N):
      values = [int(s) for s in FileasList[n].split() if s.isdigit()]
      w =values[0]
      h = values[1]
      totarea += h*w
      rects.append([w,h])
      results.append([w,h])
    solved,(t_tot,t_solve),(m,c,H) = solve(rects,W,totarea,opt=False)
    if solved:
      for r in range(len(rects)):
        results[r].append(c[r][0])
        results[r].append(c[r][1])
      fileout = f"SAT/outputs/out-{i}.txt"
      with open(fileout, "w") as file2:
        file2.write(f"{W}\n")
        file2.write(f"{N}\n")
        for i in range(len(results)):
          file2.write(f"{results[i]}\n")
      plot_result(results,W,H)
