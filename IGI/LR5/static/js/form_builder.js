document.addEventListener('DOMContentLoaded', function () {

    class RadioBuilder {
        constructor() {
            this.trigger = document.getElementById('spawn_radio_trigger');
            this.container = document.getElementById('radio_cards_container');
            this.previewBox = document.getElementById('preview_radios_box');

            if (!this.trigger || !this.container) return;

            // Достаем сохраненные данные из памяти
            this.items = JSON.parse(localStorage.getItem('radio_builder_items')) || [];

            this.init();
        }

        init() {
            this.render();

            // При нажатии на флажок создаем новую кнопку
            this.trigger.addEventListener('change', () => {
                if (this.trigger.checked) {
                    this.addNewRadio();
                    setTimeout(() => { this.trigger.checked = false; }, 200);
                }
            });
        }

        addNewRadio() {
            let uniqueId = 'radio_' + Date.now();
            let index = this.items.length + 1;

            let newItem = {
                id: uniqueId,
                name: 'payment_method',        // Общее имя группы по умолчанию
                value: 'option_' + index,      // Значение
                label: 'Option ' + index,      // Текст варианта
                checked: index === 1,          // Первая выбрана сразу
                required: false,
                disabled: false
            };

            this.items.push(newItem);
            this.saveAndRender();
        }

        // Сохраняем в память БЕЗ уничтожения полей ввода
        saveData() {
            localStorage.setItem('radio_builder_items', JSON.stringify(this.items));
        }

        // Сохраняем и полностью перерисовываем (только при добавлении/удалении)
        saveAndRender() {
            this.saveData();
            this.render();
        }

        render() {
            this.container.innerHTML = '';
            this.previewBox.innerHTML = '';

            if (this.items.length === 0) {
                this.container.innerHTML = '<p><i>No radio buttons yet. Click the checkbox above to generate!</i></p>';
                this.previewBox.innerHTML = '<p><i>Form is empty. Generate radio buttons first.</i></p>';
                return;
            }

            this.items.forEach((item, idx) => {
                // 1. Создаем карточку настроек
                let card = document.createElement('div');
                card.className = 'builder_card';
                card.innerHTML = `
                    <div class="card_header">
                        <strong>#${idx + 1} &lt;input type="radio"&gt;</strong>
                        <button class="delete_card_btn">Delete ×</button>
                    </div>

                    <div class="attr_row">
                        <label>name (group):</label>
                        <input type="text" class="input_name" value="${item.name}">
                    </div>

                    <div class="attr_row">
                        <label>value:</label>
                        <input type="text" class="input_value" value="${item.value}">
                    </div>

                    <div class="attr_row">
                        <label>label text:</label>
                        <input type="text" class="input_label" value="${item.label}">
                    </div>

                    <div class="attr_checkboxes">
                        <label><input type="checkbox" class="cb_checked" ${item.checked ? 'checked' : ''}> checked</label>
                        <label><input type="checkbox" class="cb_disabled" ${item.disabled ? 'checked' : ''}> disabled</label>
                        <label><input type="checkbox" class="cb_required" ${item.required ? 'checked' : ''}> required</label>
                    </div>

                    <div class="live_element_preview">
                        <small>Card Preview:</small>
                        <input type="radio" class="card_demo_radio" name="${item.name}_demo" ${item.checked ? 'checked' : ''} ${item.disabled ? 'disabled' : ''}>
                        <span class="card_demo_label">${item.label}</span>
                    </div>
                `;

                // 2. Создаем живой элемент для формы внизу
                let previewRow = document.createElement('label');
                previewRow.style.display = 'flex';
                previewRow.style.alignItems = 'center';
                previewRow.style.gap = '8px';
                previewRow.style.cursor = item.disabled ? 'not-allowed' : 'pointer';

                let liveRadio = document.createElement('input');
                liveRadio.type = 'radio';
                liveRadio.name = item.name;
                liveRadio.value = item.value;
                if (item.checked) liveRadio.checked = true;
                if (item.disabled) liveRadio.disabled = true;
                if (item.required) liveRadio.required = true;

                let liveText = document.createElement('span');
                liveText.textContent = `${item.label} (value="${item.value}")`;
                if (item.disabled) liveText.style.color = '#999';

                previewRow.appendChild(liveRadio);
                previewRow.appendChild(liveText);
                this.previewBox.appendChild(previewRow);

                // ==========================================
                // ИСПРАВЛЕНИЕ: МЯГКОЕ ОБНОВЛЕНИЕ БЕЗ СЛЁТА КУРСОРА
                // ==========================================
                let cardDemoRadio = card.querySelector('.card_demo_radio');
                let cardDemoLabel = card.querySelector('.card_demo_label');

                // Ввод имени группы (name)
                card.querySelector('.input_name').addEventListener('input', (e) => {
                    item.name = e.target.value;
                    liveRadio.name = item.name;
                    cardDemoRadio.name = item.name + '_demo';
                    this.saveData(); // Просто сохраняем, ничего не перерисовывая!
                });

                // Ввод значения (value)
                card.querySelector('.input_value').addEventListener('input', (e) => {
                    item.value = e.target.value;
                    liveRadio.value = item.value;
                    liveText.textContent = `${item.label} (value="${item.value}")`;
                    this.saveData();
                });

                // Ввод текста надписи (label)
                card.querySelector('.input_label').addEventListener('input', (e) => {
                    item.label = e.target.value;
                    cardDemoLabel.textContent = item.label;
                    liveText.textContent = `${item.label} (value="${item.value}")`;
                    this.saveData();
                });

                // Переключение галочки checked
                card.querySelector('.cb_checked').addEventListener('change', (e) => {
                    if (e.target.checked) {
                        this.items.forEach(other => {
                            if (other.name === item.name) other.checked = false;
                        });
                        item.checked = true;
                    } else {
                        item.checked = false;
                    }
                    this.saveAndRender();
                });

                // Переключение disabled (заблокировать)
                card.querySelector('.cb_disabled').addEventListener('change', (e) => {
                    item.disabled = e.target.checked;
                    cardDemoRadio.disabled = item.disabled;
                    liveRadio.disabled = item.disabled;
                    previewRow.style.cursor = item.disabled ? 'not-allowed' : 'pointer';
                    liveText.style.color = item.disabled ? '#999' : '';
                    this.saveData();
                });

                // Переключение required
                card.querySelector('.cb_required').addEventListener('change', (e) => {
                    item.required = e.target.checked;
                    liveRadio.required = item.required;
                    this.saveData();
                });

                // Удаление карточки
                card.querySelector('.delete_card_btn').addEventListener('click', () => {
                    this.items = this.items.filter(i => i.id !== item.id);
                    this.saveAndRender();
                });

                // Если в живой форме внизу пользователь кликает по радиокнопке
                liveRadio.addEventListener('change', () => {
                    this.items.forEach(other => {
                        if (other.name === item.name) other.checked = false;
                    });
                    item.checked = true;
                    this.saveAndRender();
                });

                this.container.appendChild(card);
            });
        }
    }

    const builder = new RadioBuilder();
});