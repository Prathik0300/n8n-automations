from flask import Flask, request, send_file
import subprocess, os, tempfile, shutil

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_latex():
    data = request.get_json()
    latex = data.get('latex', '')
    title = data.get('title', 'resume').replace('/', '_').replace(' ', '_')

    if not latex:
        return {'error': 'No LaTeX provided'}, 400

    tmpdir = tempfile.mkdtemp()
    try:
        tex_file = os.path.join(tmpdir, f'{title}.tex')
        pdf_file = os.path.join(tmpdir, f'{title}.pdf')

        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex)

        # Run pdflatex twice for proper rendering
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_file],
                capture_output=True, timeout=60
            )

        if os.path.exists(pdf_file):
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'{title}.pdf'
            )
        else:
            log = result.stdout.decode() + result.stderr.decode()
            return {'error': 'Compilation failed', 'log': log}, 500

    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
