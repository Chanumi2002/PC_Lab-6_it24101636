#!/usr/bin/env python3
"""Run performance experiments. Requires MPI installed and compiled binaries."""
import argparse, csv, pathlib, math, statistics, subprocess, shutil

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mpirun',default='mpirun')
    p.add_argument('--repeat',type=int,default=5)
    p.add_argument('--counts',type=int,nargs='+',default=[1,2,4,8])
    p.add_argument('--output',default='results/benchmark.csv')
    p.add_argument('--timeout',type=float,default=120,help='Maximum seconds per MPI run')
    args=p.parse_args()
    if args.repeat < 1 or not math.isfinite(args.timeout) or args.timeout <= 0 or any(n < 1 for n in args.counts):
        p.error('repeat, timeout, and process counts must be positive')
    if not args.counts or args.counts[0] != 1 or len(set(args.counts)) != len(args.counts):
        p.error('counts must start with 1 and contain no duplicates')
    root=pathlib.Path(__file__).resolve().parent.parent
    for tool in (args.mpirun, 'timeout'):
        if not shutil.which(tool):
            p.error(f'Required tool not found: {tool}. Run inside Ubuntu WSL with MPI installed.')
    for program in ('ex2_sum', 'ex3_pi'):
        if not (root/'build'/program).is_file():
            p.error(f'Missing build/{program}; run python3 scripts/test_lab.py first')
    output=root/args.output;output.parent.mkdir(parents=True,exist_ok=True)
    raw_path=output.with_name(output.stem+'_raw.csv')
    def save_raw():
        with raw_path.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['exercise','processors','run','seconds','result','stdout','stderr']);writer.writeheader();writer.writerows(raw)
    rows=[]; raw=[]
    for program in ('ex2_sum','ex3_pi'):
        baseline=None
        for n in args.counts:
            times=[]; values=[]
            for i in range(args.repeat):
                cmd=['timeout','--kill-after=2s',f'{args.timeout}s',args.mpirun,'-n',str(n),str(root/'build'/program)]
                proc=subprocess.run(cmd,text=True,capture_output=True,timeout=args.timeout+10)
                if proc.returncode != 0:
                    raise RuntimeError(f'MPI run failed (exit {proc.returncode}): {cmd}\n{proc.stdout}\n{proc.stderr}')
                line=next((line for line in proc.stdout.splitlines() if line.startswith('exercise=')),None)
                if not line: raise ValueError(f'No data from {cmd}: {proc.stdout} {proc.stderr}')
                parsed=dict(field.split('=',1) for field in line.split(','))
                if int(parsed['processes']) != n:
                    raise ValueError(f'Unexpected process count: {line}')
                if program == 'ex2_sum' and int(parsed['result']) != 50000005000000:
                    raise ValueError(f'Incorrect sum: {line}')
                if program == 'ex3_pi':
                    estimate=float(parsed['result']); inside=int(parsed['inside'])
                    if (not math.isfinite(estimate) or abs(estimate-math.pi)>0.005
                        or int(parsed['samples']) != 10000000 or not 0 <= inside <= 10000000
                        or abs(estimate-4*inside/10000000)>1e-10):
                        raise ValueError(f'Invalid Pi result: {line}')
                if not math.isfinite(float(parsed['time'])) or float(parsed['time']) <= 0:
                    raise ValueError(f'Invalid time: {line}')
                times.append(float(parsed['time']));values.append(parsed['result'])
                raw.append({'exercise':program,'processors':n,'run':i+1,'seconds':parsed['time'],'result':parsed['result'],'stdout':proc.stdout,'stderr':proc.stderr})
                save_raw()
            median=statistics.median(times)
            average=statistics.mean(times)
            if n==1:baseline=average
            if baseline is None:raise ValueError('Include 1 in --counts for speedup baseline')
            rows.append({'exercise':program,'processors':n,'average_seconds':average,'median_seconds':median,'speedup':baseline/average,'result':values[-1]})
            print(rows[-1])
    with output.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['exercise','processors','average_seconds','median_seconds','speedup','result']);writer.writeheader();writer.writerows(rows)
    print('Saved',output)
if __name__=='__main__':main()
