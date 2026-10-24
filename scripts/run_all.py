"""Reproduce S1, S2, Molina from frozen source cards in any working directory."""
from pathlib import Path
import json, shutil, subprocess, sys, platform, importlib.metadata
from verify_outputs import verify_inputs,verify_results,ROOT

SCRIPTS=['replay_s1.py','replay_s2_reconstructed.py','replay_molina.py']

def main():
    print('Python',sys.version.split()[0],'OS',platform.platform())
    for mod in ('numpy','scipy','scikit-learn'):
        print(mod,importlib.metadata.version(mod))
    print('Checking unchanged historical inputs ...')
    if verify_inputs()!=6:raise AssertionError('Expected exactly six frozen hashes')
    work=ROOT/'work'
    if work.exists():shutil.rmtree(work)
    work.mkdir()
    for f in (ROOT/'data/frozen').iterdir():shutil.copy2(f,work/f.name)
    for script in SCRIPTS:
        print('Running',script,flush=True)
        cp=subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT/'work',capture_output=True,text=True,check=False)
        if cp.returncode:print(cp.stdout);print(cp.stderr,file=sys.stderr);raise RuntimeError(f'{script} failed ({cp.returncode})')
    cp=subprocess.run([sys.executable,str(ROOT/'scripts/reproduce_threshold_transfer.py')],cwd=ROOT/'work',capture_output=True,text=True)
    if cp.returncode:raise RuntimeError('threshold transfer rebuild failed: '+cp.stderr)
    # run comparisons, with no modifications to archived original results.
    n=verify_results()
    (ROOT/'results/reproduced').mkdir(parents=True,exist_ok=True)
    report={'status':'PASS','input_hashes_checked':6,'experiments':3,'outcome_rows_verified':n,
            'python':sys.version.split()[0],'numpy':importlib.metadata.version('numpy'),
            'scipy':importlib.metadata.version('scipy'),'scikit_learn':importlib.metadata.version('scikit-learn'),
            'notes':'S2 runner is reconstructed from archived S1 scoring procedure. Frozen datasets/protocols untouched.'}
    (ROOT/'results/reproduced/VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    for f in work.iterdir():
        if f.name=='threshold_transfer_diagnostic.csv' or f.name.endswith(('_results_v1.json','_results_v2.json','_results_v3.json','_results_v1.csv','_results_v2.csv','_results_v3.csv','_score_drops_v1.csv','_score_drops_v3.csv')):
            shutil.copy2(f,ROOT/'results/reproduced'/f.name)
    print('SUCCESS: all archived outputs reproduced; report in results/reproduced/VERIFICATION.json')

if __name__=='__main__':
    try:main()
    except Exception as e:print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
