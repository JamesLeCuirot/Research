"""Clear the document metadata of the built PDF (AAAI anonymous-submission instruction: "The PDF
document's metadata should be cleared with a metadata-cleaning tool before submitting it").
Copies only the pages (and what they reference) into a new file, so no Info dictionary, XMP
stream or orphaned object survives; removes pdfTeX's PTEX.* keys; keeps PDF version 1.5."""
import sys
from pypdf import PdfReader, PdfWriter
src, dst = sys.argv[1:3]
r = PdfReader(src)
n = 0
for page in r.pages:                # strip PTEX.* keys before anything is copied

    res = page.get('/Resources')
    xo = res.get_object().get('/XObject') if res is not None else None
    if xo is None:
        continue
    for name, ref in xo.get_object().items():
        x = ref.get_object()
        for k in [k for k in x.keys() if k.startswith('/PTEX')]:
            del x[k]; n += 1
w = PdfWriter()
for p in r.pages:
    w.add_page(p)
w._info = None                      # no Info dictionary in the trailer
w.pdf_header = r.pdf_header         # keep %PDF-1.5
w.write(dst)
print('pages', len(w.pages), '| PTEX keys removed', n, '| header', r.pdf_header)
