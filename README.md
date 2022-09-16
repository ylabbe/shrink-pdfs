# shrink-pfds
Reduce the size of pdf figures in your latex project using `ghostscript`.

# Installation
- Install ghostscript, make sure `gs` is in your `$PATH`
- `pip install git+https://github.com/ylabbe/shrink-pdfs`


# Usage
`shrink-pdfs /path/to/my-directory`

This will scrap all pdfs stored in directories named `figures/`.
For each pdf, a compressed version `my-pdf-name_compressed.pdf` is created.
