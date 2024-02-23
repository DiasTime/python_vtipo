const express = require('express');
const fs = require('fs');

const app = express();
app.use(express.static('public'));
app.use(express.json());

const users = JSON.parse(fs.readFileSync('users.json'));

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

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
