const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;

// Подключение к MongoDB через Mongoose
mongoose.connect(MONGO_URI)
    .then(() => console.log('Successfully connected to MongoDB!'))
    .catch((err) => console.error('Connection error to MongoDB:', err));

// Тестовый маршрут
app.get('/', (req, res) => {
    json_response = { message: "Bookstore API is running successfully!" };
    res.json(json_response);
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});