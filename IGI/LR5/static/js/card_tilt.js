class Card3DTilt {
    constructor(cardSelector = '.book_card', maxAngle = 18) {
        this.cards = document.querySelectorAll(cardSelector);
        this.maxAngle = maxAngle;

        this.init();
    }

    init() {
        this.cards.forEach(card => {
            card.addEventListener('mousemove', (e) => this.handleMouseMove(e, card));
            card.addEventListener('mouseleave', () => this.handleMouseLeave(card));
            card.addEventListener('mouseenter', () => this.handleMouseEnter(card));
        });
    }

    handleMouseEnter(card) {
        card.style.transition = 'transform 0.08s ease-out, box-shadow 0.2s ease';
    }

    handleMouseMove(e, card) {
        const rect = card.getBoundingClientRect();
        
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        const rotX = -y * this.maxAngle * 2;
        const rotY = x * this.maxAngle * 2;

        card.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.05, 1.05, 1.05)`;

        const shadowX = -x * 25;
        const shadowY = -y * 25 + 15;
        card.style.boxShadow = `${shadowX}px ${shadowY}px 25px rgba(0, 0, 0, 0.2)`;
    }

    handleMouseLeave(card) {
        card.style.transition = 'transform 0.5s ease-out, box-shadow 0.5s ease';
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        card.style.boxShadow = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Card3DTilt('.book_card', 15);
});