from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from Crypto.Cipher import AES
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# AES key (must be 16, 24, or 32 bytes long)
SECRET_KEY = b'secretkey1234567'

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Function to decrypt messages
def decrypt_message(encrypted_message):
    try:
        cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=encrypted_message[:16])
        decrypted_message = cipher.decrypt(encrypted_message[16:])
        return decrypted_message.decode('utf-8')
    except Exception as e:
        print("Decryption failed:", e)
        return "[Decryption failed]"

# Handle incoming messages
@socketio.on('chat_message')
def handle_chat_message(encrypted_message_base64):
    encrypted_message = base64.b64decode(encrypted_message_base64)
    decrypted_message = decrypt_message(encrypted_message)
    print("Decrypted message:", decrypted_message)
    emit('chat_message', decrypted_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
