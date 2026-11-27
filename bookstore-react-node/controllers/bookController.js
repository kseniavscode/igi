const Book = require('../models/Book');

const getAllBooks = async (req, res) => {
    try {
        const books = await Book.find().populate('author', 'name country birthDate');
        res.json(books);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};