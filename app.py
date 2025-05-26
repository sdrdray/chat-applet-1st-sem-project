from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room
from Crypto.Cipher import AES
import base64
import binascii

app = Flask(__name__)
socketio = SocketIO(app)

# AES key for encryption
key = b'\xda\x0f\xe3\xb8*\xf9\xa8~\xbe9Bp[c\xc0Ef\x9d\x9a{\x9cmB\xa3\x97q(\x0b\x0e\x10KU'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    join_room(data['client_id'])
    print(f"Client {data['client_id']} joined their room")

@socketio.on('send_message')
def handle_message(data):
    nonce = base64.b64decode(data['nonce'])
    encrypted_message = base64.b64decode(data['message'])
    
    # Display the encrypted message
    print(f"Encrypted message (hex): {binascii.hexlify(encrypted_message)}")

    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, nonce)
    decrypted_message = cipher.decrypt(encrypted_message)
    decrypted_message = decrypted_message[:-decrypted_message[-1]]
    
    try:
        decrypted_message = decrypted_message.decode('utf-8')
        print(f"Decrypted message: {decrypted_message}")
    except UnicodeDecodeError:
        print("Decrypted message is not valid UTF-8")

    socketio.emit('message', data, room=data['to'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
