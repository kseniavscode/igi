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
            email: 'admin@bookstore.com',
            password: 'admin1234',
            role: 'admin'
        });

        const manager = await User.create({
            username: 'manager',
            email: 'manager@bookstore.com',
            password: 'manager1234',
            role: 'manager'
        });

        const user = await User.create({
            username: 'user',
            email: 'user@mail.ru',
            password: '123456',
            role: 'user'
        });

        console.log('Users created.');  

        const author1 = await Author.create({
            name: 'Ray Bradbury',
            country: 'USA',
            birthDate: new Date('1920-08-22'),
            biography: 'American author and screenwriter.'
        });

        const author2 = await Author.create({
            name: 'Lev Tolstoy',
            country: 'Russia',
            birthDate: new Date('1828-09-09'),
            biography: 'Master of realistic fiction.'
        });

        const author3 = await Author.create({
            name: 'Stephen King',
            country: 'USA',
            birthDate: new Date('1947-09-21'),
            biography: 'King of horror.'
        });
        console.log('Authors created.');

        const books = await Book.create([
            {
                isbn: '9780007136551',
                title: 'Fahrenheit 451',
                author: author1._id,
                genre: 'Sci-Fi',
                price: 22.50,
                stock: 15,
                publicationDate: new Date('1953-10-19'),
                description: 'A dystopian novel about book burning.'
            },
            {
                isbn: '9780553296358',
                title: 'The Martian Chronicles',
                author: author1._id,
                genre: 'Sci-Fi',
                price: 19.99,
                stock: 8,
                publicationDate: new Date('1950-05-04'),
                description: 'Chronicles of human settlement on Mars.'
            },
            {
                isbn: '9780199232765',
                title: 'War and Peace',
                author: author2._id,
                genre: 'Classic',
                price: 45.00,
                stock: 5,
                publicationDate: new Date('1869-01-01'),
                description: 'Historical novel spanning the Napoleonic era.'
            },
            {
                isbn: '9780140447934',
                title: 'Anna Karenina',
                author: author2._id,
                genre: 'Classic',
                price: 28.00,
                stock: 10,
                publicationDate: new Date('1878-01-01'),
                description: 'A tragic novel of infidelity.'
            },
            {
                isbn: '9781501142970',
                title: 'The Shining',
                author: author3._id,
                genre: 'Detective',
                price: 24.99,
                stock: 12,
                publicationDate: new Date('1977-01-28'),
                description: 'Horror novel about an isolated winter caretaker.'
            },
            {
                isbn: '9781476754406',
                title: 'It',
                author: author3._id,
                genre: 'Classic',
                price: 32.50,
                stock: 7,
                publicationDate: new Date('1986-09-15'),
                description: 'An evil entity haunts children in Maine.'
            },
            {
                isbn: '9780307743657',
                title: 'Doctor Sleep',
                author: author3._id,
                genre: 'Classic',
                price: 21.00,
                stock: 9,
                publicationDate: new Date('2013-09-24'),
                description: 'Sequel to The Shining.'
            },
            {
                isbn: '9780553213103',
                title: 'Resurrection',
                author: author2._id,
                genre: 'Classic',
                price: 18.50,
                stock: 6,
                publicationDate: new Date('1899-01-01'),
                description: 'The last novel published by Leo Tolstoy.'
            },
            {
                isbn: '9780451524935',
                title: '1984',
                author: author1._id,
                genre: 'Sci-Fi',
                price: 20.00,
                stock: 25,
                publicationDate: new Date('1949-06-08'),
                description: 'Dystopian social science fiction novel.'
            },
            {
                isbn: '9780743273565',
                title: 'The Great Gatsby',
                author: author2._id,
                genre: 'Classic',
                price: 15.00,
                stock: 18,
                publicationDate: new Date('1925-04-10'),
                description: 'Novel of the Jazz Age in New York.'
            }
        ]);
        console.log(`${books.length} books created.`);

        await Order.create({
            user: user._id,
            items: [
                {
                    book: books[0]._id,
                    quantity: 2,
                    price: books[0].price
                }
            ],
            totalAmount: books[0].price * 2,
            status: 'pending'
        });
        console.log('Order created.');

        console.log('Database seeding completed successfully!');
        process.exit(0);

    }
    catch (error) {
        console.error('Error during database seeding:', error);
        process.exit(1);
    }
}

seedDatabase();
