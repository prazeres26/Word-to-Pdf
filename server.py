from flask import Flask, request, send_file
import requests, os, time

app = Flask(__name__)
CLOUDCONVERT_API_KEY = os.getenv("CLOUDCONVERT_API_KEY", "sua_chave_aqui")

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    input_filename = file.filename
    file.save(input_filename)

    # 1. Import
    import_task = requests.post('https://api.cloudconvert.com/v2/import/upload',
        headers={'Authorization': f'Bearer {CLOUDCONVERT_API_KEY}'}).json()
    upload_url = import_task['data']['result']['form']['url']
    upload_params = import_task['data']['result']['form']['parameters']
    with open(input_filename, 'rb') as f:
        requests.post(upload_url, data=upload_params, files={'file': (input_filename, f)})
    import_id = import_task['data']['id']

    # 2. Convert
    output_format = 'pdf' if input_filename.endswith(('.doc', '.docx')) else 'docx'
    convert_task = requests.post('https://api.cloudconvert.com/v2/tasks',
        json={
            'operation': 'convert',
            'input': import_id,
            'input_format': input_filename.split('.')[-1],
            'output_format': output_format
        },
        headers={'Authorization': f'Bearer {CLOUDCONVERT_API_KEY}'}
    ).json()
    task_id = convert_task['data']['id']

    # 3. Wait
    while True:
        status = requests.get(f'https://api.cloudconvert.com/v2/tasks/{task_id}',
                              headers={'Authorization': f'Bearer {CLOUDCONVERT_API_KEY}'}).json()
        if status['data']['status'] == 'finished': break
        if status['data']['status'] == 'error': return 'Erro na conversão', 500
        time.sleep(2)

    # 4. Download
    file_url = status['data']['result']['files'][0]['url']
    output_file = f'convertido.{output_format}'
    with open(output_file, 'wb') as out:
        out.write(requests.get(file_url).content)
    os.remove(input_filename)
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
