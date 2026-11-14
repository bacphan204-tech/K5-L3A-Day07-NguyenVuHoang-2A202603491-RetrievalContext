"""Build and index a transparent 120-page source excerpt, retaining original page mapping."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def printed_page_number(page,original_pdf_page):
    numbers=[word for word in page.get_text('words') if word[1]<42 and word[4].isdigit()]
    if not numbers:
        raise ValueError(f'No printed page number found on original PDF page {original_pdf_page}.')
    word=min(numbers,key=lambda item:item[0]) if original_pdf_page%2==0 else max(numbers,key=lambda item:item[2])
    return int(word[4])

def main():
    import pymupdf
    original=ROOT/'.local/advanced_source_full.pdf'
    source=pymupdf.open(original)
    selected=list(range(25,129))+[409,410,427,428,463,464,583,584,667,668,670,671,685,686,696,697]
    assert len(selected)==len(set(selected))==120
    excerpt=pymupdf.open()
    for number in selected:
        excerpt.insert_pdf(source,from_page=number-1,to_page=number-1)
    pdf=ROOT/'data/advanced/economics-120-pages.pdf'
    excerpt.save(pdf,garbage=4,deflate=True)
    excerpt.close()
    doc=pymupdf.open(pdf)
    pages=[]; chunks=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        printed_page=printed_page_number(page,selected[i])
        pages.append({'page':i+1,'original_pdf_page':selected[i],'printed_page':printed_page,'text':text,'width':page.rect.width,'height':page.rect.height,
                      'image_objects':len(page.get_images()),'drawing_objects':len(page.get_drawings())})
        for start in range(0,len(text),2200):
            value=text[start:start+2600]
            if value.strip():
                chunks.append({'id':f'fullbook:p{i+1}:c{start}', 'text':value,'source_id':'openstax-economics-3e-full',
                   'source':'data/advanced/economics-120-pages.pdf','page':i+1,
                   'metadata':{'original_pdf_page':selected[i],'printed_page':printed_page,'page_bbox':[0,0,page.rect.width,page.rect.height],'start_char':start,'end_char':start+len(value)}})
    folder=ROOT/'data/advanced'
    for name,value in [('pages.json',pages),('chunks.json',chunks),('manifest.json',{
        'title':'Principles of Economics 3e','publisher':'OpenStax, Rice University','source_url':'https://openstax.org/details/books/principles-economics-3e/',
        'download_url':'https://assets.openstax.org/oscms-prodcms/media/documents/principles-economics-3e_-_WEB.pdf',
        'license':'CC BY-NC-SA 4.0; retain the original copyright pages and individual figure credits',
        'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'physical_pages':len(doc),'indexed_text_pages':sum(bool(p['text'].strip()) for p in pages),
        'document_scope':'Student-compiled 120-page excerpt, not a standalone original OpenStax publication. Chapters 1-5 plus selected financial-system diagrams and surrounding text.',
        'original_pdf_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'original_page_mapping':selected,
        'rights_notice':'Copyright/license notice retained separately from original page 4; do not represent the compilation as the full book.',
        'chunks':len(chunks),'unindexed_text_pages':[p['page'] for p in pages if not p['text'].strip()],
        'visual_access':'All original pages available for on-demand rendering; figures/drawings not replaced by OCR guesses.',
        'limits':'Text/caption index does not semantically index unlabeled pixels; selected pages must be inspected by vision and source reviewer.'})]:
        (folder/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Indexed',len(doc),'pages;',len(chunks),'chunks. Original visual pages retained.')
    notice=pymupdf.open()
    notice.insert_pdf(source,from_page=3,to_page=3)
    notice.save(folder/'copyright-notice.pdf')

if __name__=='__main__': main()
