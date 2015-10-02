import os
import subprocess
import json
import tempfile
from flask import Flask, request, make_response

# Path to the codegen bianry, built by the Dockerfile
codegen_path = os.path.abspath("../echoprint-codegen")

app = Flask(__name__)
# Set debug to True for testign
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def get_fingerprint():
    """
    Send a file with MIME type "multipart/form-data" with a POST method, in the field "file", to the root of the app.
    It will return back the JSON code generated by Echoprint Codegen.

    If you access the root of the app with a GET method (as in a web browser) you'll receive a simple form to submit the
    data. Useful for debugging.
    """
    if request.method == 'POST':
        f = request.files['file']
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        f.save(temp.name)
        resp = make_response(json.dumps(codegen(temp.name)))
        os.remove(temp.name)
        return resp
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

def codegen(file, start=None, duration=None):
    """
    Generate the response from the Echoprint Codegen as a parsed JSON.

    :param file: audio file path to generate the fingerprint for
    :param start: start time in seconds, to be passed to codegen
    :param duration: duration of fingerprint to extract
    :return: parsed JSON returned by Echoprint Codegen binary
    """
    proclist = [codegen_path, os.path.abspath(file)]
    if start:
        proclist.append("%d" % start)
        if duration:
            proclist.append("%d" % duration)
    if not start and duration:
        proclist.append("0")
        proclist.append("%d" % duration)
    p = subprocess.Popen(proclist, stdout=subprocess.PIPE)
    code = p.communicate()[0]
    return json.loads(code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
