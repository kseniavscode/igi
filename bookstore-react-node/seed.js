const mongoose = require('mongoose');
require('dotenv').config();

const MONGO_URI = process.env.MONGO_URI;

const User = require('./models/User');
const Author = require('./models/Author');
const Book = require('./models/Book');
const Order = require('./models/Order');

async function seedDatabase() {
    try {
        await mongoose.connect(MONGO_URI);
        console.log('MongoDB connected successfully!');

        await User.deleteMany({});
        await Author.deleteMany({});
        await Book.deleteMany({});
        await Order.deleteMany({});

        const admin = await User.create({
            username: 'admin',
            email: 'admin@book_store.com',
            password: 'admin1234',
            role: 'admin'
        });

        const manager = await User.create({
            username: 'manager',
            email: 'manager@book_store.com',
            password: 'manager1234',
            role: 'manager'
        });

        const user = await User.create({
            username: 'user',
            email: 'user@mail.ru',
            password: '1234',
            role: 'user'
        });

    }
    catch (error) {
        console.error('Error during database seeding:', error);
        process.exit(1);
    }
}

seedDatabase();
