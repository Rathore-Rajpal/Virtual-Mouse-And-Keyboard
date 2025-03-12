from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/launch-mouse', methods=['POST'])
def launch_virtual_mouse():
    try:
        # Launch the virtualMouse.py script
        subprocess.Popen(['python', 'C://VirtualMouseProject//virtualMouse.py'])
        return jsonify({'message': 'Virtual Mouse Launched!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/launch-keyboard', methods=['POST'])
def launch_virtual_keyboard():
    try:
        # Launch the virtual_keyboard.py script
        subprocess.Popen(['python', 'C://VirtualMouseProject//virtual_ketboard.py'])
        return jsonify({'message': 'Virtual Keyboard Launched!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
