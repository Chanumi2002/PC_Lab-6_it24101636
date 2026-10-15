#!/usr/bin/env python3
import csv,pathlib
import matplotlib.pyplot as plt
root=pathlib.Path(__file__).resolve().parent.parent
with (root/'results'/'benchmark.csv').open() as f: rows=list(csv.DictReader(f))
out=root/'results'/'graphs';out.mkdir(parents=True,exist_ok=True)
for exercise in ('ex2_sum','ex3_pi'):
 data=sorted((r for r in rows if r['exercise']==exercise),key=lambda r:int(r['processors']))
 x=[int(r['processors']) for r in data]
 for field,label,suffix in [('average_seconds','Average execution time (seconds)','time'),('speedup','Speedup (T1/Tp)','speedup')]:
  y=[float(r[field]) for r in data]
  fig,ax=plt.subplots();ax.plot(x,y,marker='o',label='Measured')
  if suffix=='speedup':ax.plot(x,x,linestyle='--',label='Ideal');ax.legend()
  ax.set_xlabel('Number of MPI processes');ax.set_ylabel(label)
  ax.set_title(f'{exercise}: {label}');ax.set_xticks(x);ax.grid(True,alpha=.25)
  fig.tight_layout();fig.savefig(out/f'{exercise}_{suffix}.png',dpi=160);plt.close(fig)
  print('Saved',out/f'{exercise}_{suffix}.png')
