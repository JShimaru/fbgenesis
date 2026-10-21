import pdfplumber
p=r'C:\Users\yamit\Downloads\Create a Multiplayer Game _ Learn.pdf'
with pdfplumber.open(p) as d:
 print('PAGES',len(d.pages))
 for i,page in enumerate(d.pages):
  print(f'--- PAGE {i+1} ---')
  print(page.extract_text() or '')
