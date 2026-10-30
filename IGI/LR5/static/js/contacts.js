document.addEventListener('DOMContentLoaded', function () {
    
    const employeesDataElement = document.getElementById('employees_data');
    if (!employeesDataElement) return;
    
    let rawData = JSON.parse(employeesDataElement.textContent);

    let tableData = rawData.map(item => ({
        id: item.pk,
        full_name: item.fields.full_name,
        position: item.fields.position,
        email: item.fields.email,
        phone: item.fields.phone || 'N/A',
        description: item.fields.description || 'No description',
        photo: item.fields.photo ? '/media/' + item.fields.photo : null
    }));

    let currentPage = 1;
    let itemsPerPage = 3; 
    let currentSortColumn = null;
    let sortDirection = 'asc'; 
    let filteredData = [...tableData];

    const tableBody = document.getElementById('table_body');
    const paginationBox = document.getElementById('paginationBox');
    const searchInput = document.getElementById('search_input');
    const searchBtn = document.getElementById('search_btn');
    const resetSearchBtn = document.getElementById('reset_search_btn');
    const detailsBox = document.getElementById('detailsBox');
    const detailsContent = document.getElementById('detailsContent');
    const preloader = document.getElementById('preloader');

    function renderTable() {
        tableBody.innerHTML = '';

        const selectAllCheckbox = document.getElementById('select_all');
        if (selectAllCheckbox) {
            selectAllCheckbox.checked = false;
        }

        let start = (currentPage - 1) * itemsPerPage;
        let end = start + itemsPerPage;
        let pageItems = filteredData.slice(start, end);

        if (pageItems.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No employees found</td></tr>`;
            paginationBox.innerHTML = '';
            return;
        }

        pageItems.forEach(emp => {
            let row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="checkbox" class="emp_checkbox" data-id="${emp.id}"></td>
                <td><img src="${emp.photo || '/static/images/book_cover_default.jpg'}" alt="photo" width="40" height="40" style="object-fit:cover; border-radius:50%;"></td>
                <td>${emp.full_name}</td>
                <td>${emp.position}</td>
                <td>${emp.email}</td>
                <td>${emp.phone}</td>
            `;

            row.addEventListener('click', (e) => {
                if (e.target.tagName === 'INPUT') return; 
                showDetails(emp);
            });

            tableBody.appendChild(row);
        });

        renderPagination();
    }

    function renderPagination() {
        paginationBox.innerHTML = '';
        let totalPages = Math.ceil(filteredData.length / itemsPerPage);
        if (totalPages <= 1) return;

        for (let i = 1; i <= totalPages; i++) {
            let btn = document.createElement('button');
            btn.textContent = i;
            btn.className = 'panel_btn' + (i === currentPage ? ' active_page' : '');
            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
            });
            paginationBox.appendChild(btn);
        }
    }

    function showDetails(emp) {
        detailsBox.style.display = 'block';
        detailsContent.innerHTML = `
            <p><strong>Name:</strong> ${emp.full_name}</p>
            <p><strong>Position:</strong> ${emp.position}</p>
            <p><strong>Description:</strong> ${emp.description}</p>
            <p><strong>Email:</strong> ${emp.email}</p>
            <p><strong>Phone:</strong> ${emp.phone}</p>
        `;
    }

    const selectAllCheckbox = document.getElementById('select_all');

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const rowCheckboxes = document.querySelectorAll('.emp_checkbox');
            
            rowCheckboxes.forEach(cb => {
                cb.checked = selectAllCheckbox.checked;
            });
        });
    }

    document.querySelectorAll('.sortable').forEach(th => {
        th.style.cursor = 'pointer';

        th.addEventListener('click', () => {
            let column = th.getAttribute('data-sort');
            if (!column) return; 

            if (currentSortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortColumn = column;
                sortDirection = 'asc';
            }

            document.querySelectorAll('.sortable').forEach(el => {
                let name = el.getAttribute('data-name') || el.textContent.replace(/[↕▲▼]/g, '').trim();
                el.setAttribute('data-name', name); 
                el.textContent = name + ' ↕';
            });

            let cleanName = th.getAttribute('data-name');
            th.textContent = cleanName + (sortDirection === 'asc' ? ' ▲' : ' ▼');

            filteredData.sort((a, b) => {
                let valA = a[column] ? String(a[column]).toLowerCase() : '';
                let valB = b[column] ? String(b[column]).toLowerCase() : '';

                if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
                if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            currentPage = 1;
            renderTable();
        });
    });

    searchBtn.addEventListener('click', () => {
        showPreloader();
        setTimeout(() => { 
            let query = searchInput.value.toLowerCase().trim();
            filteredData = tableData.filter(emp => 
                emp.full_name.toLowerCase().includes(query) ||
                emp.position.toLowerCase().includes(query) ||
                emp.email.toLowerCase().includes(query)
            );
            currentPage = 1;
            renderTable();
            hidePreloader();
            resetSearchBtn.style.display = 'inline-block';
        }, 400);
    });

    resetSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        filteredData = [...tableData];
        currentPage = 1;
        renderTable();
        resetSearchBtn.style.display = 'none';
    });

    // Управление прелоадером
    function showPreloader() { preloader.style.display = 'block'; }
    function hidePreloader() { preloader.style.display = 'none'; }

    // Кнопка Премировать (чекбоксы)
    document.getElementById('award_btn').addEventListener('click', () => {
        let checkedBoxes = document.querySelectorAll('.emp_checkbox:checked');
        let awardedNames = [];

        checkedBoxes.forEach(cb => {
            let id = parseInt(cb.getAttribute('data-id'));
            let emp = tableData.find(e => e.id === id);
            if (emp) awardedNames.push(emp.full_name);
        });

        let resultBox = document.getElementById('award_result');
        if (awardedNames.length > 0) {
            resultBox.innerHTML = `<strong>🏆 Awarded employees:</strong> ${awardedNames.join(', ')}. Congratulations!`;
        } else {
            resultBox.innerHTML = `<i>Please select at least one employee using checkboxes.</i>`;
        }
    });

    // Выпадающая форма добавления
    const toggleFormBtn = document.getElementById('toggle_form_btn');
    const formContainer = document.getElementById('add_employee_form_container');
    toggleFormBtn.addEventListener('click', () => {
        formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
    });

    // ВАЛИДАЦИЯ URL и ТЕЛЕФОНА (Требование методички)
    const phoneInput = document.getElementById('phone_input');
    const phoneError = document.getElementById('phone_error');
    const urlInput = document.getElementById('url_input');
    const urlError = document.getElementById('url_error');
    const submitBtn = document.getElementById('submit_employee_btn');

    const phoneRegex = /^(?:\+375|8)\s*(?:\(\s*0?\d{2}\s*\)|0?\d{2})\s*\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    
    // URL: начинается с http:// или https://, заканчивается на .php или .html
    const urlRegex = /^(http:\/\/|https:\/\/).+\.(php|html)$/;

    function checkPhoneAndUrl(phoneValue, urlValue) {
        let isPhoneValid = phoneRegex.test(phoneValue.trim());
        
        // URL валиден, если он пустой (необязателен) ИЛИ подходит под критерии методички
        let isUrlValid = urlValue.trim() === '' || urlRegex.test(urlValue.trim());

        return {
            phoneValid: isPhoneValid,
            urlValid: isUrlValid,
            allValid: isPhoneValid && isUrlValid
        };
    }

    function validateForm() {
        let phoneVal = phoneInput.value;
        let urlVal = urlInput.value;

        // Передаем в функцию и получаем результат
        let result = checkPhoneAndUrl(phoneVal, urlVal);

        // --- ПРОВЕРКА ТЕЛЕФОНА ---
        if (phoneVal.trim() === '') {
            // Если поле пустое
            phoneInput.style.border = '';
            phoneInput.style.backgroundColor = '';
            phoneError.textContent = '';
        } else if (!result.phoneValid) {
            // РОЗОВЫЙ ФОН И КРАСНАЯ ГРАНИЦА ПО ЗАДАНИЮ
            phoneInput.style.border = '2px solid red';
            phoneInput.style.backgroundColor = '#ffcccc'; // Светло-розовый
            phoneError.style.color = 'red';
            phoneError.textContent = 'Invalid phone format! Example: 8(029)1112233 or +375 (29) 111-22-33';
        } else {
            // Валидно
            phoneInput.style.border = '2px solid green';
            phoneInput.style.backgroundColor = '#e8f5e9'; // Светло-зеленый
            phoneError.style.color = 'green';
            phoneError.textContent = 'Phone number is valid ✓';
        }

        // --- ПРОВЕРКА URL ---
        if (urlVal.trim() === '') {
            urlInput.style.border = '';
            urlInput.style.backgroundColor = '';
            urlError.textContent = '';
        } else if (!result.urlValid) {
            // РОЗОВЫЙ ФОН И КРАСНАЯ ГРАНИЦА ПО ЗАДАНИЮ
            urlInput.style.border = '2px solid red';
            urlInput.style.backgroundColor = '#ffcccc';
            urlError.style.color = 'red';
            urlError.textContent = 'URL must start with http:// or https:// and end with .php or .html';
        } else {
            urlInput.style.border = '2px solid green';
            urlInput.style.backgroundColor = '#e8f5e9';
            urlError.style.color = 'green';
            urlError.textContent = 'URL is valid ✓';
        }

        // Кнопка разблокируется, только если введен валидный телефон и валидный URL
        submitBtn.disabled = !result.allValid || phoneVal.trim() === '';
    }

    phoneInput.addEventListener('input', validateForm);
    urlInput.addEventListener('input', validateForm);

    // Первый запуск отрисовки таблицы
    renderTable();

    // ==========================================
    // ДОБАВЛЕНИЕ НОВОГО СОТРУДНИКА ЧЕРЕЗ JS
    // ==========================================
    const employeeForm = document.getElementById('employee_form');
    
    if (employeeForm) {
        employeeForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Останавливаем стандартную перезагрузку страницы
            
            showPreloader(); // Включаем твой прелоадер из ЛР2!

            let formData = new FormData(employeeForm);

            // Отправляем данные на сервер (текущий URL страницы)
            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Говорим Django, что это AJAX-запрос
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                hidePreloader(); // Выключаем прелоадер

                if (data.status === 'success') {
                    // Успех! Добавляем нового сотрудника в наш массив tableData
                    let newEmp = {
                        id: data.employee.id,
                        full_name: data.employee.full_name,
                        position: data.employee.position,
                        email: data.employee.email,
                        phone: data.employee.phone || 'N/A',
                        description: data.employee.description || 'No description',
                        photo: data.employee.photo ? data.employee.photo : null
                    };

                    tableData.push(newEmp);     // Добавляем в общую копилку
                    filteredData = [...tableData]; // Обновляем фильтр
                    renderTable();              // Перерисовываем таблицу!

                    // Очищаем форму и закрываем её
                    employeeForm.reset();
                    document.getElementById('add_employee_form_container').style.display = 'none';
                    alert('Employee added successfully!');
                } else {
                    alert('Error adding employee. Check fields.');
                }
            })
            .catch(error => {
                hidePreloader();
                console.error('Error:', error);
                alert('Something went wrong!');
            });
        });
    }
});

