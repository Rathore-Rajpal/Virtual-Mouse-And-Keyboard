from flask import Flask, request, jsonify
from CodeBot import generate_code
from flask_cors import CORS
from datetime import datetime  # <-- New import here
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Empty prompt', 'code': ''}), 400
        
    try:
        generated_code = generate_code(prompt)
        if not generated_code.strip():
            return jsonify({'error': 'Empty code generated', 'code': ''}), 500
            
        return jsonify({
            'code': generated_code,
            'error': '',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f"Backend Error: {str(e)}",
            'code': '',
            'timestamp': datetime.now().isoformat()
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)