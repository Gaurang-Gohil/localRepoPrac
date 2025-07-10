import subprocess
import os

def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Compress a PDF using Ghostscript.
    
    Args:
        input_path (str): Path to input PDF.
        output_path (str): Path to save compressed PDF.
        quality (str): Ghostscript quality: screen, ebook, printer, prepress, default.
    """
    qualities = ['screen', 'ebook', 'printer', 'prepress', 'default']
    if quality not in qualities:
        raise ValueError(f"Quality must be one of: {qualities}")

    try:
        subprocess.run([
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS=/{quality}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            input_path
        ], check=True)

        final_size_kb = os.path.getsize(output_path) / 1024
        print(f"\n✅ Compression done. Compressed file size: {final_size_kb:.2f} KB")

    except FileNotFoundError:
        print("❌ Ghostscript not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ghostscript error: {e}")

if __name__ == "__main__":
    print("🔍 PDF Compressor")
    input_pdf = input("Enter full path of the PDF to compress: ").strip().strip('"')

    if not os.path.isfile(input_pdf):
        print("❌ File not found. Please check the path.")
        exit(1)

    # Default temporary output path
    temp_output = "compressed_temp.pdf"
    
    # Compress the file
    compress_pdf(input_pdf, temp_output, quality='ebook')

    # Ask for final filename
    new_name = input("\nEnter a new name for the compressed PDF (without .pdf): ").strip()
    final_output = f"{new_name}.pdf"

    try:
        os.rename(temp_output, final_output)
        print(f"✅ Saved compressed PDF as: {final_output}")
    except Exception as e:
        print(f"❌ Failed to rename file: {e}")
