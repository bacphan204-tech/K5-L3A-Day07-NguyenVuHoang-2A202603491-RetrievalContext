"""Package code/evidence; omit secrets and local runtimes."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from llm_client import read_settings


def main():
    folders=('artifacts','assets','benchmark','data','docs','report','results','scripts','src','starter','tests')
    rootfiles=('README.md','.gitignore','.gitattributes','.env.example','requirements.txt','requirements-lock.txt',
               'ADVANCED.md','AGENT_SETUP.md','BENCHMARK.md','CHECKPOINTS.md','GUIDE.md','PSEUDOCODE.md','REPORT_TEMPLATE.md','RUBRIC.md','RULES.md','SUBMISSION.md')
    selected=[ROOT/name for name in rootfiles if (ROOT/name).is_file()]
    for folder in folders:
        selected.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and not any(x in ('.venv','__pycache__','.local','.git') for x in p.parts) and p.suffix!='.pyc' and not p.name.startswith('.env'))
    try: key=read_settings()['api_key'].encode()
    except ValueError: key=None
    files=[]
    for p in sorted(set(selected)):
        content=p.read_bytes()
        if key and key in content:
            raise ValueError('Credential detected in submission; value not printed.')
        if p.suffix in ('.json','.jsonl','.md','.py','.ps1','.txt') and re.search(rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{30,}',content):
            raise ValueError('Possible credential detected; value not printed.')
        files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)})
    out=ROOT/'submission'
    out.mkdir(exist_ok=True)
    archive=out/'Day07_2A202603491_NguyenVuHoang.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for entry in files: z.write(ROOT/entry['path'],entry['path'])
        z.writestr('SUBMISSION_MANIFEST.json',json.dumps({'files':files,'credentials_excluded':True,'local_runtimes_excluded':True},indent=2))
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None: raise ValueError('Archive integrity check failed')
        assert '.env' not in z.namelist()
    (out/'manifest.json').write_text(json.dumps({'archive':archive.name,'file_count':len(files),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
             'credential_scan':'passed; no key values logged','exclusions':['.env','.local','venv','.git','__pycache__']},indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {archive} | files={len(files)} | bytes={archive.stat().st_size} | no credentials/local runtimes')


if __name__=='__main__': main()
