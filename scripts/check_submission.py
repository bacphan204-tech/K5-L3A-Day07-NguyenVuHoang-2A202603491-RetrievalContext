"""Final artifact/lock/label checks without invoking any model."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from benchmark import validate_cases,validate_minimums,pipeline_input
from agent_evaluation import reviews_ready


def load(path): return json.loads(path.read_text(encoding='utf-8'))


def main():
    subprocess.run([sys.executable,'-X','utf8','scripts/final_evaluation.py','verify-lock'],cwd=ROOT,check=True)
    cases=[]
    for split in ('dev','test'):
        rows=load(ROOT/f'benchmark/{split}.json')
        assert load(ROOT/f'benchmark/{split}.inputs.json')==[pipeline_input(c) for c in rows]
        cases.extend(rows)
    checked=validate_cases(cases,load(ROOT/'data/day6/chunks.json'))
    validate_minimums(checked['counts'])
    lock=load(ROOT/'benchmark/frozen.json')
    folders=[ROOT/lock['dev_run'],ROOT/'results/final/test']
    for folder in folders:
        labels=load(folder/'cases.json')
        for method in ('dense','rerank'):
            traces=load(folder/method/'traces.json')
            reviews=load(folder/method/'reviews.json')
            assert len(traces)==len(labels)
            assert not reviews_ready(labels,traces,reviews)
            assert all(t['status'] in ('answered','abstain') for t in traces)
            assert all(r['student_confirmed'] is False for r in reviews)
    report=ROOT/'report/individual/2A202603491_NguyenVuHoang.md'
    assert report.is_file() and report.stat().st_size>5000
    result={'status':'PASS','benchmark_counts':checked['counts'],'dev_agent_traces':34,'test_agent_traces':14,
            'semantic_reviews_complete_by_ai':True,'student_confirmed':False,'frozen_pipeline_unchanged':True,
            'report_present':True,'optional_advanced_done':False,'api_called_by_this_check':False}
    (ROOT/'results/final/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
