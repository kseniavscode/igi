// ==========================================
// КЛАСС ДЛЯ 3D-ПАРАЛЛАКСА КАРТОЧЕК (Задание 6)
// ==========================================
class Card3DTilt {
    constructor(cardSelector = '.book_card', maxAngle = 18) {
        // 1. Находим все карточки книг в каталоге
        this.cards = document.querySelectorAll(cardSelector);
        // Максимальный угол наклона в градусах
        this.maxAngle = maxAngle;

        this.init();
    }

    init() {
        this.cards.forEach(card => {
            // При движении мышки внутри карточки — наклоняем
            card.addEventListener('mousemove', (e) => this.handleMouseMove(e, card));
            
            // Мышка ушла — возвращаем карточку на место ровно в 0 градусов
            card.addEventListener('mouseleave', () => this.handleMouseLeave(card));
            
            // Мышка вошла — делаем реакцию мгновенной (без задержек)
            card.addEventListener('mouseenter', () => this.handleMouseEnter(card));
        });
    }

    handleMouseEnter(card) {
        // Убираем длинную задержку, чтобы карточка моментально следовала за курсором
        card.style.transition = 'transform 0.08s ease-out, box-shadow 0.2s ease';
    }

    handleMouseMove(e, card) {
        // 1. Получаем точные координаты и размеры карточки на экране
        const rect = card.getBoundingClientRect();
        
        // 2. Вычисляем положение курсора от центра карточки:
        // x и y получаются от -0.5 (слева/сверху) до +0.5 (справа/снизу)
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        // 3. Считаем углы наклона:
        // Если курсор идет вверх (y < 0), верх карточки наклоняется к нам (rotateX > 0)
        const rotX = -y * this.maxAngle * 2;
        const rotY = x * this.maxAngle * 2;

        // 4. Наклоняем карточку в 3D и чуть увеличиваем масштаб
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