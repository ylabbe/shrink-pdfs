import argparse
from ctypes import sizeof
import os
from pathlib import Path
import logging
import glob
import subprocess
import pathlib
from tqdm import tqdm

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def run_ghostscript(
    input: pathlib.Path, 
    output: pathlib.Path):
    command = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSettings=/printer',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output}',
        str(input)
    ]
    completed = subprocess.run(command)
    assert output.exists()
    return

def should_run_on_filename(filename: str, excludes=["compressed"]):
    if not filename.endswith(".pdf"):
        return False

    for exclude in excludes:
        if exclude in filename:
            return False

    return True

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser("shrink-pdfs")
    parser.add_argument("project_dir", type=pathlib.Path)
    parser.add_argument("--filename-suffix", type=str, default="_compressed")
    parser.add_argument("--dry-run", action='store_true')
    args = parser.parse_args()
    pdf_files = []
    for dirname, dirnames, fnames in os.walk(args.project_dir):
        dirpath = Path(dirname)
        if dirpath.name == 'figures':
            pdf_files += [dirpath / fname for fname in fnames if 
                          should_run_on_filename(fname, excludes=[args.filename_suffix])]

    pbar = tqdm(pdf_files, disable=True)
    for pdf_file in pbar:
        pdf_path = Path(pdf_file)
        pbar.set_postfix({'file': str(pdf_path.name)})
        pdf_path_output = pdf_path.parent / (pdf_path.with_suffix('').name + args.filename_suffix + '.pdf')
        run_ghostscript(pdf_path, pdf_path_output)
        input_size = pdf_path.stat().st_size
        output_size = pdf_path_output.stat().st_size
        diff_percent = 100 * (input_size - output_size) / input_size
        input_size_str = sizeof_fmt(input_size)
        output_size_str = sizeof_fmt(output_size)
        print(f"{pdf_path.name} -> {pdf_path_output.name}; {input_size_str} -> {output_size_str} ({diff_percent:.1f} %)")

if __name__ == '__main__':
    main()