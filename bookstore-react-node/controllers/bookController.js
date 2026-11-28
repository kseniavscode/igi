const Book = require('.../models/Book');
const Author = require('...models/Author');

const getOrCreateAuthor = async (authorName, authorCountry, authorBio, authorBirthDate) => {

    let author = await Author.findOne({
        name: {$regex: new RegExp('^' + authorName + '$', 'i')}
    });

    if (!author) {
        author = await Author.create({ 
            name: authorName, 
            country: authorCountry, 
            biography: authorBio, 
            birthDate: authorBirthDate });
    }
    return author._id;
};

const getAllBooks = async (req, res) => {
    try{
        const {search, sort} = req.query;
        let query = {};

        if (search) {

            const finedAuthor = await Author.find({
                name: {$regex: search, $options: 'i'}
            });
            const authorIds = finedAuthor.map(author => author._id);

            query = {
                $or: [
                    { title: { $regex: search, $options: 'i' } },
                    { genre: { $regex: search, $options: 'i' } },
                    { author: { $in: finedAuthor }}
                ]
            };
        }

        let sortOptions = {};
        if (sort) {
            if (sort === 'title_asc') {
                sortOptions = { title: 1 };
            } 
            else if (sort === 'title_desc') {
                sortOptions = { title: -1 };
            }
            else if (sort === 'price_asc') {
                sortOptions = { price: 1 };
            }
            else if (sort === 'price_desc') {
                sortOptions = { price: -1 };
            }
            else sortOption = { createdAt: -1 };
        }
        const books = await Book.find(query).sort(sortOptions).populate('author');
        res.status(200).json(books);
    }
    catch (e){
        res.status(400).json({
            message: e.message
        })
    }
};

const getBookById = async (req, res) => {
    try{
        const {id} = req.params;
        const book = await Book.findById(id).populate('author');
        if (!book) {
            return res.status(404).json({
                message: 'Book not found'
            });
        }
        res.status(200).json(book);
    }
    catch (e) {
        res.status(404).json({
            message: e.message
        })
    }
};

const createBook = async (req, res) => {
    try{
        const {authorName, authorCountry, authorBio, authorBirthDate, ...bookData} = req.body;
        let authorId = bookData.author;
        if (!authorId && authorName){
            authorId = await getOrCreateAuthor(authorName, authorCountry, authorBio, authorBirthDate);
        }
        const book = await Book.create({
            ...bookData, author: authorId
        });
        res.status(201).json(book);
    }
    catch (e) {
        res.status(400).json({
            message: e.message
        })
    }
};

const deleteBook = async (req, res) =>{
    try{
        const {id} = req.params;
        const book = await Book.findByIdAndDelete(id);
        if (!book) {
            return res.status(404).json({
                message: 'Book not found'
            });
        }
        res.status(200).json({
            message: 'Book deleted successfully'
        });
    }
    catch (e) {
        res.status(404).json({
            message: e.message
        })
    }
};

module.exports = {
    getOrCreateAuthor,
    getAllBooks,
    getBookById,
    createBook,
    deleteBook
};