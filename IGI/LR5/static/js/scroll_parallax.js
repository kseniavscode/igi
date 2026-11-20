class VintageLibraryParallax {
    constructor(sectionId = 'vintageParallax') {
        this.section = document.getElementById(sectionId);
        if (!this.section) return;

        this.bg = this.section.querySelector('.layer_bg');
        this.leftBooks = this.section.querySelector('.layer_left_books');
        this.rightBooks = this.section.querySelector('.layer_right_books');
        this.centerBook = this.section.querySelector('.layer_center_book');
        this.textLayer = this.section.querySelector('.layer_text');

        this.ticking = false; 

        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            if (!this.ticking) {
                window.requestAnimationFrame(() => {
                    this.updateParallax();
                    this.ticking = false;
                });
                this.ticking = true;
            }
        });

        this.updateParallax();
    }

    updateParallax() {
        const rect = this.section.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        if (rect.top <= windowHeight && rect.bottom >= 0) {
            
            const progress = (windowHeight - rect.top) / (windowHeight + rect.height);
            const normalizedProgress = (0.5 - progress) * 2;
            const bgY = -normalizedProgress * 35;
            this.bg.style.transform = `scale(1.15) translateY(${bgY}px)`;

            const leftX = (progress - 0.5) * -160;
            const leftRot = (progress - 0.5) * -8;
            this.leftBooks.style.transform = `translateX(${leftX}px) rotate(${leftRot}deg)`;

            const rightX = (progress - 0.5) * 160;
            const rightRot = (progress - 0.5) * 8;
            this.rightBooks.style.transform = `translateX(${rightX}px) rotate(${rightRot}deg)`;

            const centerY = 150 + (progress - 0.5) * 220; 
            const centerScale = 0.8 + (progress * 0.8);  
            const centerRot = (progress - 0.5) * 16;      
            this.centerBook.style.transform = `translateY(${centerY}px) scale(${centerScale}) rotate(${centerRot}deg)`;

            const textY = (0.5 - progress) * -90;
            const textOpacity = 1 - Math.abs(normalizedProgress) * 0.7; 
            this.textLayer.style.transform = `translateY(${textY}px)`;
            this.textLayer.style.opacity = Math.max(0.2, textOpacity);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VintageLibraryParallax('vintageParallax');
});