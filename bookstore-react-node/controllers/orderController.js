const Order = require('../models/Order');

const createOrder = async (req, res) => {
    try {
        const { user, items, totalAmount } = req.body;
        const newOrder = await Order.create({ user, items, totalAmount, status: 'pending' });
        res.status(201).json(newOrder);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

const getOrders = async (req, res) => {
    try {
        const { userId } = req.query;
        let query = userId ? { user: userId } : {};

        const orders = await Order.find(query).populate('user', 'username email').populate('items.book', 'title price');
        res.json(orders);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

const updateOrderStatus = async (req, res) => {
    try {
        const { status, cancellationReason, isPaid } = req.body;
        
        let updateData = { status };
        if (cancellationReason) updateData.cancellationReason = cancellationReason;
        if (isPaid !== undefined) {
            updateData.isPaid = isPaid;
            if (isPaid) updateData.paidAt = new Date();
        }

        const updatedOrder = await Order.findByIdAndUpdate(req.params.id, updateData, { new: true, runValidators: true });
        if (!updatedOrder) return res.status(404).json({ message: 'Order not found' });

        res.json(updatedOrder);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

module.exports = { 
    createOrder, 
    getOrders, 
    updateOrderStatus 
};