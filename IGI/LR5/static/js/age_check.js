document.addEventListener('DOMContentLoaded', function () {
    class AgeVerifier {
        constructor() {
            this.modal = document.getElementById('age_modal_overlay');
            this.dateInput = document.getElementById('birth_date_input');
            this.submitBtn = document.getElementById('check_age_btn');
            this.resultBox = document.getElementById('age_result_box');
            this.closeBtn = document.getElementById('close_age_modal_btn');
            this.openBtn = document.getElementById('open_age_check_btn');

            this.daysOfWeek = [
                'воскресенье',
                'понедельник',
                'вторник',
                'среду',
                'четверг',
                'пятницу',
                'субботу'
            ];

            this.init();
        }

        init() {
            const isAlreadyAnswered = localStorage.getItem('user_age_confirmed');

            if (!isAlreadyAnswered && this.modal) {
            // if (this.modal) {
                setTimeout(() => {
                    this.openModal();
                }, 800);
            }

            if (this.submitBtn) {
                this.submitBtn.addEventListener('click', () => this.verifyAge());
            }

            if (this.closeBtn) {
                this.closeBtn.addEventListener('click', () => this.closeModal());
            }

            if (this.openBtn) {
                this.openBtn.addEventListener('click', () => this.openModal());
            }
        }

        openModal() {
            if (this.modal) {
                this.modal.style.display = 'flex';
                this.resultBox.style.display = 'none';
            }
        }

        closeModal() {
            if (this.modal) {
                this.modal.style.display = 'none';
            }
        }

        verifyAge() {
            const rawDate = this.dateInput.value;
            if (!rawDate) {
                alert('Пожалуйста, выберите дату рождения в календаре!');
                return;
            }

            const birthDate = new Date(rawDate);
            const today = new Date();

            if (birthDate > today) {
                alert('Дата рождения не может быть в будущем!');
                return;
            }

            let age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }

            const dayIndex = birthDate.getDay();
            const dayName = this.daysOfWeek[dayIndex];

            localStorage.setItem('user_age_confirmed', 'true');

            if (age >= 18) {
                this.resultBox.className = 'age_result_box age_result_adult';
                this.resultBox.innerHTML = `
                    <strong>Доступ разрешён!</strong><br>
                    Вам полных лет: <strong>${age}</strong>.<br>
                    Вы родились в <strong>${dayName}</strong>.<br>
                    Приятных покупок в книжном магазине!
                `;
                this.resultBox.style.display = 'block';

                setTimeout(() => {
                    this.closeModal();
                }, 2500);

            } else {
                alert('Внимание! Вам ' + age + ' лет. Для использования сайта книжного магазина и покупок необходимо разрешение родителей!');

                this.resultBox.className = 'age_result_box age_result_minor';
                this.resultBox.innerHTML = `
                    <strong>Внимание!</strong><br>
                    Вам полных лет: <strong>${age}</strong> (несовершеннолетний).<br>
                    Для покупок на сайте требуется согласие родителей.
                `;
                this.resultBox.style.display = 'block';
            }
        }
    }

    new AgeVerifier();
});