class VintageLibraryParallax {
    constructor(sectionId = 'vintageParallax') {
        this.section = document.getElementById(sectionId);
        if (!this.section) return;

        // Находим все движущиеся слои
        this.bg = this.section.querySelector('.layer_bg');
        this.leftBooks = this.section.querySelector('.layer_left_books');
        this.rightBooks = this.section.querySelector('.layer_right_books');
        this.centerBook = this.section.querySelector('.layer_center_book');
        this.textLayer = this.section.querySelector('.layer_text');

        this.ticking = false; // Флаг для requestAnimationFrame (60 FPS)

        this.init();
    }

    init() {
        // Слушаем событие скролла окна
        window.addEventListener('scroll', () => {
            if (!this.ticking) {
                // requestAnimationFrame делает анимацию плавной без рывков
                window.requestAnimationFrame(() => {
                    this.updateParallax();
                    this.ticking = false;
                });
                this.ticking = true;
            }
        });

        // Первый вызов при загрузке страницы
        this.updateParallax();
    }

    updateParallax() {
        const rect = this.section.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        // Проверяем: видна ли секция в окне браузера прямо сейчас?
        if (rect.top <= windowHeight && rect.bottom >= 0) {
            
            // 🌟 ВЫЧИСЛЯЕМ ПРОГРЕСС СКРОЛЛА (от 0 до 1):
            // 0 = секция только показалась снизу экрана
            // 0.5 = секция ровно по центру экрана
            // 1 = секция уходит вверх за пределы экрана
            const progress = (windowHeight - rect.top) / (windowHeight + rect.height);
            
            // Смещение относительно центра экрана (-1 до +1)
            const normalizedProgress = (0.5 - progress) * 2;

            // =====================================================
            // ДВИЖЕНИЕ СЛОЕВ (ПРИ СКРОЛЛЕ ВНИЗ И ОБРАТНО ВВЕРХ!):
            // =====================================================

            // 1. Фон: медленно плывет вниз по вертикали
            const bgY = -normalizedProgress * 35;
            this.bg.style.transform = `scale(1.15) translateY(${bgY}px)`;

            // 2. Левая полка с книгами: выезжает слева к центру
            // При скролле вниз сдвигается вправо, при скролле вверх — уезжает обратно влево!
            const leftX = (progress - 0.5) * -160;
            const leftRot = (progress - 0.5) * -8;
            this.leftBooks.style.transform = `translateX(${leftX}px) rotate(${leftRot}deg)`;

            // 3. Правая полка: выезжает справа к центру
            const rightX = (progress - 0.5) * 160;
            const rightRot = (progress - 0.5) * 8;
            this.rightBooks.style.transform = `translateX(${rightX}px) rotate(${rightRot}deg)`;

            // 4. Центральная парящая книга: поднимается навстречу и плавно покачивается в 3D
            const centerY = 150 + (progress - 0.5) * 220; 
            const centerScale = 0.8 + (progress * 0.8);   // Активный рост масштаба
            const centerRot = (progress - 0.5) * 16;       // лёгкий 3D наклон
            this.centerBook.style.transform = `translateY(${centerY}px) scale(${centerScale}) rotate(${centerRot}deg)`;

            // 5. Текст: всплывает снизу вверх с эффектом изменения прозрачности
            const textY = (0.5 - progress) * -90;
            const textOpacity = 1 - Math.abs(normalizedProgress) * 0.7; // ярче всего по центру экрана
            this.textLayer.style.transform = `translateY(${textY}px)`;
            this.textLayer.style.opacity = Math.max(0.2, textOpacity);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VintageLibraryParallax('vintageParallax');
});