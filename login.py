from flask import Flask, request, redirect

app = Flask(__name__)

def authenticate(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            data = line.strip().split(':')
            if data[0] == username and data[1] == password:
                return data[2]  # Возвращаем тип пользователя (student или teacher)
    return None

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_type = authenticate(username, password)
    if user_type == 'student':
        return redirect('http://127.0.0.1:5001')
    elif user_type == 'teacher':
        return redirect('http://127.0.0.1:5000')
    else:
        return "Invalid username or password"

if __name__ == '__main__':
    app.run(debug=True)
