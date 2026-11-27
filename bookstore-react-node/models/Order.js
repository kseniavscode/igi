const mongoose = require('mongoose');

const OrderItemSchema = new mongoose.Schema({
    book: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Book',
        required: [true, 'Book reference is required']
    },
    quantity: {
        type: Number,
        required: [true, 'Quantity is required'],
        min: [1, 'Quantity must be at least 1'],
        validate: {
            validator: Number.isInteger,
            message: 'Quantity must be an integer'
        }
    },
    price: {
        type: Number,
        required: [true, 'Price is required'],
        min: [0, 'Price cannot be negative']
    }
});

const OrderSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: [true, 'User reference is required']
    },
    items: {
        type: [OrderItemSchema],
        required: [true, 'Order items are required'],
        validate: {
            validator: function(v) {
                return v &&v.length > 0;
            },
            message: 'Order must contain at least one item'
        }   
    },
    totalAmount: {
        type: Number,
        required: [true, 'Total amount is required'],
        min: [0, 'Total amount cannot be negative']
    },
    status: {
        type: String,
        enum: {
            values: ['pending', 'processing', 'completed', 'cancelled'],
            message: 'Status "{VALUE}" is not supported'
        },
        default: 'pending'
    }
},
{
    timestamps: true
});

module.exports = mongoose.model('Order', orderSchema);