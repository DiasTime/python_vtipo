const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.static('public'));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
const users = JSON.parse(fs.readFileSync('users.json'));

const PORT = 1000; // Новый порт

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(user => user.username === username && user.password === password);
    
    if (user) {
        if (user.type === 'student') {
            res.json({ redirectUrl: 'http://127.0.0.1:5001' });
        } else if (user.type === 'teacher') {
            res.json({ redirectUrl: 'http://127.0.0.1:5000' });
        }
    } else {
        res.status(401).json({ message: 'Invalid username or password' });
    }
});

app.listen(PORT, () => { // Изменение порта здесь
    console.log(`Server is running on port ${PORT}`);
});
// app.get('/1', (req, res) => {
//     res.send('Hello, this is the homepage');
// });
