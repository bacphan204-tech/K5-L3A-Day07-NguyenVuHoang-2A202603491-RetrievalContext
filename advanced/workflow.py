"""Separate advanced benchmark authoring and real multimodal retrieval experiments."""
import argparse,base64,hashlib,json,re,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from llm_client import ResponsesClient,read_settings
from book_agent import tool
from lexical_retrieval import BM25Retriever
from freeze import runtime_settings

HERE=ROOT/'advanced'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_test_lock(vision,test_name):
 lock_path=HERE/('frozen.json' if test_name=='test' else f'frozen-{test_name}.json')
 lock=load(lock_path)
 if lock.get('vision')!=vision:
  raise ValueError('Test vision setting differs from the frozen configuration.')
 expected={
  'inputs_sha256':digest(HERE/'benchmark'/f'{test_name}.inputs.json'),
  'gold_sha256':digest(HERE/'benchmark'/f'{test_name}.json'),
  'chunks_sha256':digest(ROOT/'data/advanced/chunks.json'),
  'pages_sha256':digest(ROOT/'data/advanced/pages.json'),
  'source_pdf_sha256':digest(ROOT/'data/advanced/economics-120-pages.pdf'),
  'code_sha256':{
   'workflow.py':digest(HERE/'workflow.py'),
   'llm_client.py':digest(ROOT/'src/llm_client.py'),
   'lexical_retrieval.py':digest(ROOT/'src/lexical_retrieval.py')},
  'model_settings':runtime_settings()}
 for key,value in expected.items():
  if lock.get(key)!=value:
   raise ValueError(f'Frozen test integrity check failed: {key}')

def image(page):
 import pymupdf
 doc=pymupdf.open(ROOT/'data/advanced/economics-120-pages.pdf')
 data=doc[page-1].get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).tobytes('jpeg')
 doc.close()
 return {'type':'input_image','image_url':'data:image/jpeg;base64,'+base64.b64encode(data).decode(),'detail':'high'}
def client():
 s=read_settings();s['max_output_tokens']=2400
 return ResponsesClient(s)
def author():
 pages=load(ROOT/'data/advanced/pages.json');mapping={p['original_pdf_page']:p['page'] for p in pages}
 seeds={
 'dev':{'table':[[38],[67],[88]],'diagram':[[583],[686],[697]],'chart':[[45],[81],[108]],'multi_hop':[[65,67],[33,671],[112,668]],'text':[[26],[47],[76]]},
 'test':{'table':[[65],[72],[81],[103],[109],[112]],'diagram':[[33],[409],[428],[464],[668]],'chart':[[50],[68],[85],[111],[128]],'multi_hop':[[33,428],[65,112],[50,464],[668,697]],'text':[[30],[35],[89],[104]]}}
 schema=tool('publish_case','Publish one source-supported Vietnamese question.',{'question':{'type':'string'},'expected_answer':{'type':'string'},'evidence_description':{'type':'string'}})
 for split,groups in seeds.items():
  output=HERE/'benchmark'/f'{split}.json'
  cases=load(output) if output.exists() else []
  for group,lists in groups.items():
   for n,originals in enumerate(lists,1):
    cid=f'adv-{split}-{group}-{n:02}'
    if any(c['id']==cid for c in cases):continue
    selected=[mapping[x] for x in originals]
    instruction=f'Create ONE Vietnamese benchmark question in category {group}. Use the supplied ORIGINAL page images as authority; do not invent or use external knowledge. Include explicit Figure/Table numbers when asking about visual items so the question is self-contained. Ask a real nontrivial but unambiguous question. Table: exact row/column, units and optionally calculation. Diagram: read actual arrows/labels/relationships, never decorative photo. Chart: axes, legend and values/trend. Multi_hop: MUST require information from ALL supplied pages, not two alternative sources. Text: ask a conditional fact from this page. Expected answer must be complete, exact units/conditions/calculation. Describe figure/table region clearly. Do not merely ask the page number. This is authoring, not running the answering pipeline.'
    content=[{'type':'input_text','text':instruction}]
    for p in selected:
     content += [{'type':'input_text','text':f'Excerpt page {p}; original PDF page {pages[p-1]["original_pdf_page"]}.\n'+pages[p-1]['text']},image(p)]
    c=client();_,answer=c.call([{'role':'user','content':content}],[schema],force_tool='publish_case')
    cases.append({'id':cid,'split':split,'group':group,'answerable':True,**answer,'gold_pages':selected,
       'original_pages':originals,'source':'data/advanced/economics-120-pages.pdf','review_status':'AI-authored; source-image review pending'})
    save(output,cases);save(HERE/'authoring_traces'/f'{cid}.json',{'calls':c.calls,'usage':c.usage()})
    print(cid,'authored',flush=True)
  for n,topic in enumerate(['mức lương tối thiểu vùng I Việt Nam năm 2026','giá xăng Hà Nội ngày 14/11/2026','lãi suất vay mua nhà Vietcombank tháng 11/2026'] + ([] if split=='dev' else ['tỷ lệ lạm phát Việt Nam tháng 10/2026','GDP Việt Nam quý III/2026','tỷ lệ thất nghiệp Hà Nội năm 2026']),1):
   cid=f'adv-{split}-unanswerable-{n:02}'
   if not any(c['id']==cid for c in cases): cases.append({'id':cid,'split':split,'group':'unanswerable','answerable':False,'question':f'Dựa riêng vào tài liệu, {topic} chính xác là bao nhiêu?','expected_answer':'Không đủ bằng chứng; không đoán con số.','gold_pages':[],'absence_reason':'Excerpt textbook has no contemporary Vietnam-specific dataset; full corpus scope/term and source review required.'})
  save(output,cases)
  save(HERE/'benchmark'/f'{split}.inputs.json',[{k:c[k] for k in ('id','question','group')} for c in cases])
def run(split,vision,test_name='test',run_name=None):
 benchmark_name='dev' if split=='dev' else test_name
 if split=='test':verify_test_lock(vision,benchmark_name)
 cases=load(HERE/'benchmark'/f'{benchmark_name}.inputs.json')
 pages=load(ROOT/'data/advanced/pages.json');chunks=load(ROOT/'data/advanced/chunks.json');index=BM25Retriever(chunks)
 search=tool('search_book','Choose up to three English lexical search queries for the provided question; retain figure/table IDs.',{'queries':{'type':'array','items':{'type':'string'}}})
 finish=tool('finish','Answer from the supplied source context, use excerpt-page IDs for pages, and abstain when evidence is insufficient.',{'status':{'type':'string','enum':['answered','abstain']},'answer':{'type':'string'},'pages':{'type':'array','items':{'type':'integer'},'description':'Excerpt-page IDs from supplied context only; use an empty array when abstaining.'}})
 directory=HERE/'runs'/(run_name or f'{split}-{"vision" if vision else "text"}')
 directory.mkdir(parents=True,exist_ok=True)
 for item in cases:
  destination=directory/f'{item["id"]}.json'
  if destination.exists():continue
  c=client();start=time.perf_counter();trace={'id':item['id'],'question':item['question'],'vision':vision}
  try:
   call,args=c.call([{'role':'user','content':'Search this economics textbook to answer in Vietnamese: '+item['question']}],[search],force_tool='search_book')
   queries=args['queries'][:3]; scores={}
   for query in queries:
    for rank,row in enumerate(index.search(query,top_k=40),1): scores[row['page']]=scores.get(row['page'],0)+1/(60+rank)
   # An explicit Figure/Table reference is user-provided retrieval information, not gold.
   refs=re.findall(r'(?:Figure|Table|Hình|Bảng)\s*(\d+\.\d+)',item['question'],re.I)
   for ref in refs:
    for p in pages:
     if re.search(r'(?:FIGURE|TABLE)\s+'+re.escape(ref)+r'\b',p['text'],re.I):scores[p['page']]=scores.get(p['page'],0)+1
   chosen=sorted(scores,key=lambda p:(-scores[p],p))[:6]
   context=[{'page':p,'printed_page':pages[p-1]['printed_page'],'original_pdf_page':pages[p-1]['original_pdf_page'],'text':pages[p-1]['text']} for p in chosen]
   content=[{'type':'input_text','text':'Answer the question using ONLY supplied source evidence, in Vietnamese. Include every requested subpart, condition, calculation and unit. If the source explicitly states the requested value, reproduce it instead of recalculating with assumptions (for example, do not assume weeks worked per year). For table quantities, use the quantity unit established by the relevant axis or source text, not the unit of a price column. Cite each fact with its excerpt page and printed book page; use the actual Figure/Table ID for visual evidence, and cite the section/paragraph (not a nearby image) for prose. Cite only pages that directly support your answer. The pages array MUST contain excerpt page numbers from the supplied context only, never printed or original PDF page numbers. Do not cite unsupported pages or add irrelevant claims. If evidence is insufficient, abstain without guessing. '+item['question']+'\nSOURCE_CONTEXT:'+json.dumps(context,ensure_ascii=False)}]
   if vision:
    for p in chosen:content += [{'type':'input_text','text':f'Source image: excerpt page {p}'},image(p)]
   _,final=c.call([{'role':'user','content':content}],[finish],force_tool='finish')
   trace.update(final=final,context=context,retrieval_queries=queries,ranked_pages=sorted(scores.items(),key=lambda x:-x[1]),status='success')
   valid_pages=(
    final['status']=='abstain' and set(final['pages'])<=set(chosen)
    or final['status']=='answered' and bool(final['pages']) and set(final['pages'])<=set(chosen))
   trace['citation_pages_valid']=valid_pages
   if not valid_pages:
    trace.update(status='error',error_type='ValueError',error='Citation pages are not excerpt-page IDs from the supplied context.')
  except Exception as e:trace.update(status='error',error_type=type(e).__name__,error=str(e))
  trace.update(calls=c.calls,usage=c.usage(),seconds=time.perf_counter()-start)
  save(destination,trace);print(item['id'],trace['status'],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['author','dev-text','dev-vision','dev-vision-v2','test','test-v2']);a=p.parse_args()
 if a.stage=='author':author()
 elif a.stage=='test':run('test',True)
 elif a.stage=='test-v2':run('test',True,'test-v2','test-v2-vision')
 else:run('dev',a.stage!='dev-text',run_name='dev-vision-v2' if a.stage=='dev-vision-v2' else None)
