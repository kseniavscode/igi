const mongoose = require('mongoose');

const AuthorSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Name is required'],
        trim: true,
        minlength: [2, 'Name must be at least 2 characters long'],
        maxlength: [100, 'Name cannot exceed 100 characters'],
        validate: {
            validator: function(v) {
                return /^[a-zA-Z\s]+$/.test(v);
            },
            message: 'Name can only contain letters and spaces'
        }
    },
    country: {
        type: String,
        trim: true,
        default: 'Unknown'
    },
    birthDate: {
        type: Date,
        min: [1000, 'Birth year is too old'],
        max: [new Date().getFullYear(), 'Birth year cannot be in the future']
    },
    biography: {
        type: String,
        maxlength: [2000, 'Biography is too long'],
        default: ''
    }
},
{
    timestamps: true
});

module.exports = mongoose.model('Author', AuthorSchema);