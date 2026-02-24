const express = require('express');
const mongoose = require('mongoose');
const app = express();

const dbUri = process.env.DB_URI || 'mongodb://localhost:27017/testdb';

console.log('Connecting to DB at:', dbUri); 

mongoose.connect(dbUri, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('MongoDB Connected Successfully!'))
.catch(err => console.error('MongoDB Connection Error:', err));

app.get('/', (req, res) => {
  res.send('Backend is running securely with Networks and Volumes!');
});

app.listen(5000, () => console.log('Server running on port 5000'));
