const mongoose = require('mongoose');

const BookSchema = new mongoose.Schema({
    isbn: {
        type: String,
        required: [true, 'ISBN is required'],
        length: [13, 'ISBN must be 13 characters long'],
        validate: {
            validator: function(v) {
                return /^\d{13}$/.test(v);
            },
            message: 'ISBN must be a 13-digit number'
        },
    },
    title: {
        type: String,
        required: [true, 'Title is required'],
        trim: true,
        minlength: [1, 'Title cannot be empty'],
        maxlength: [200, 'Title is too long'],
        validate: {
            validator: function(v) {
                return /^[a-zA-Z0-9\s\.,!?:-]+$/.test(v);
            },
            message: 'Title can only contain letters, numbers, and spaces'
        }
    },
    author: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Author',
        required: [true, 'Author is required']
    },
    publicationDate: {
        type: Date,
        required: [true, 'Publication date is required'],
        validate: {
            validator: function(v) {
                return v <= new Date();
            },
            message: 'Date cannot be in the future'
        }
    },
    genre: {
        type: String,
        required: [true, 'Select the genre'],
        enum: {
            values: ['Classic', 'Fantasy', 'Romantic', 'Detective', 'Programming', 'Other'],
            message: 'Genre "{VALUE}" is not supported. Please choose from the list.'
        },
        default: 'Other'
    },
    price: {
        type: Number,
        required: [true, 'Price is required'],
        min: [0, 'Price cannot be negative']
    },
    stock: {
        type: Number,
        default: 10,
        min: [0, 'Count of book instances cannot be negative'],
        validate: {
            validator: Number.isInteger,
            message: 'Count of book instances must be integer.'
        }
    },
    description: {
        type: String,
        trim: true,
        maxlength: [3000, 'Description cannot exceed 3000 characters'],
        default: 'No description provided.'
    },
    coverUrl: {
        type: String,
        trim: true,
        default: '/static/images/default_cover.png',
        validate: {
            validator: function(v) {
                return /^(https?:\/\/.+|\/static\/.+)\.(jpg|jpeg|png|webp|avif|gif|svg)$/i.test(v);
            },
            message: 'Cover URL must be a valid image URL (http/https) or local path (/static/...)'
        }
    }
},
{
    timestamps: true
});

module.exports = mongoose.model('Book', BookSchema);