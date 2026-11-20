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
    const selectAllCheckbox = document.getElementById('select_all');

    const employeeForm = document.getElementById('employee_form');
    const phoneInput = document.getElementById('phone_input');
    const phoneError = document.getElementById('phone_error');
    const urlInput = document.getElementById('url_input');
    const urlError = document.getElementById('url_error');
    const submitBtn = document.getElementById('submit_employee_btn');
    const formWarning = document.getElementById('form_warning');

    const fullNameInput = document.querySelector('input[name="full_name"]');
    const positionInput = document.querySelector('input[name="position"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');
    const emailInput = document.querySelector('input[name="email"]');

    let selectedEmployeeIds = new Set();

    function updateSelectAllCheckboxState() {
        if (!selectAllCheckbox) return;
        if (filteredData.length === 0) {
            selectAllCheckbox.checked = false;
            return;
        }
        selectAllCheckbox.checked = filteredData.every(emp => selectedEmployeeIds.has(String(emp.id)));
    }

    function renderTable() {
        tableBody.innerHTML = '';

        let start = (currentPage - 1) * itemsPerPage;
        let end = start + itemsPerPage;
        let pageItems = filteredData.slice(start, end);

        if (pageItems.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No employees found</td></tr>`;
            paginationBox.innerHTML = '';
            updateSelectAllCheckboxState();
            return;
        }

        pageItems.forEach(emp => {
            let isChecked = selectedEmployeeIds.has(String(emp.id)) ? 'checked' : '';

            let row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="checkbox" class="emp_checkbox" data-id="${emp.id}" ${isChecked}></td>
                <td><img src="${emp.photo || '/static/images/book_cover_default.jpg'}" alt="photo" width="40" height="40" style="object-fit:cover; border-radius:50%;"></td>
                <td>${emp.full_name}</td>
                <td>${emp.position}</td>
                <td>${emp.email}</td>
                <td>${emp.phone}</td>
            `;

            let cb = row.querySelector('.emp_checkbox');
            cb.addEventListener('change', () => {
                let idStr = String(emp.id);
                if (cb.checked) {
                    selectedEmployeeIds.add(idStr);
                } else {
                    selectedEmployeeIds.delete(idStr);
                }
                updateSelectAllCheckboxState();
            });

            row.addEventListener('click', (e) => {
                if (e.target.tagName === 'INPUT') return; 
                showDetails(emp);
            });

            tableBody.appendChild(row);
        });

        updateSelectAllCheckboxState();
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

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            if (selectAllCheckbox.checked) {
                filteredData.forEach(emp => selectedEmployeeIds.add(String(emp.id)));
            } else {
                filteredData.forEach(emp => selectedEmployeeIds.delete(String(emp.id)));
            }
            renderTable();
        });
    }

    document.querySelectorAll('.sortable').forEach(th => {
        th.style.cursor = 'pointer';

        let name = th.textContent.replace(/[↕▲▼]/g, '').trim();
        th.setAttribute('data-name', name);
        th.textContent = name + ' ↕';

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
                el.textContent = el.getAttribute('data-name') + ' ↕';
            });

            th.textContent = th.getAttribute('data-name') + (sortDirection === 'asc' ? ' ▲' : ' ▼');

            filteredData.sort((a, b) => {
                let valA = a[column] ? String(a[column]).toLowerCase() : '';
                let valB = b[column] ? String(b[column]).toLowerCase() : '';

                if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
                if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            currentPage = 1;
            renderTable();

            resetSearchBtn.style.display = 'inline-block';
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
        }, 1000);
    });

    resetSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        currentSortColumn = null;
        sortDirection = 'asc';

        document.querySelectorAll('.sortable').forEach(el => {
            el.textContent = el.getAttribute('data-name') + ' ↕';
        });
        filteredData = [...tableData];
        currentPage = 1;
        renderTable();

        if (detailsBox) {
            detailsBox.style.display = 'none';
            if (detailsContent) {
                detailsContent.innerHTML = '';
            }
        }
        
        resetSearchBtn.style.display = 'none';
    });

    function showPreloader() { preloader.style.display = 'block'; }
    function hidePreloader() { preloader.style.display = 'none'; }

    document.getElementById('award_btn').addEventListener('click', () => {
        let awardedNames = [];

        tableData.forEach(emp => {
            if (selectedEmployeeIds.has(String(emp.id))) {
                awardedNames.push(emp.full_name);
            }
        });

        let resultBox = document.getElementById('award_result');
        if (awardedNames.length > 0) {
            resultBox.innerHTML = `<strong>Awarded employees (${awardedNames.length}):</strong> ${awardedNames.join(', ')}. Congratulations!`;
        } else {
            resultBox.innerHTML = `<i>Please select at least one employee using checkboxes.</i>`;
        }
    });

    const toggleFormBtn = document.getElementById('toggle_form_btn');
    const formContainer = document.getElementById('add_employee_form_container');
    if (toggleFormBtn) {
        toggleFormBtn.addEventListener('click', () => {
            formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
        });
    }

    const phoneRegex = /^(?:\+375\s*(?:\(\s*\d{2}\s*\)|\d{2})|8\s*(?:\(\s*0?\d{2}\s*\)|0?\d{2}))\s*\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    const urlRegex = /^(http:\/\/|https:\/\/).+\.(php|html)$/;

    function checkPhoneAndUrl(phoneValue, urlValue) {
        let isPhoneValid = phoneRegex.test(phoneValue.trim());
        let isUrlValid = urlValue.trim() === '' || urlRegex.test(urlValue.trim());

        return {
            phoneValid: isPhoneValid,
            urlValid: isUrlValid,
            allValid: isPhoneValid && isUrlValid
        };
    }

    function validateForm() {
        if (!employeeForm) return; 

        let phoneVal = phoneInput ? phoneInput.value : '';
        let urlVal = urlInput ? urlInput.value : '';
        let result = checkPhoneAndUrl(phoneVal, urlVal);

        if (phoneVal.trim() === '') {
            phoneInput.style.border = '';
            phoneInput.style.backgroundColor = '';
            phoneError.textContent = '';
        } else if (!result.phoneValid) {
            phoneInput.style.border = '2px solid red';
            phoneInput.style.backgroundColor = '#ffcccc';
            phoneError.style.color = 'red';
            phoneError.textContent = 'Invalid phone format! Example: 8(029)1112233 or +375 (29) 111-22-33';
        } else {
            phoneInput.style.border = '2px solid green';
            phoneInput.style.backgroundColor = '#e8f5e9';
            phoneError.style.color = 'green';
            phoneError.textContent = 'Phone number is valid ✓';
        }

        if (urlVal.trim() === '') {
            urlInput.style.border = '';
            urlInput.style.backgroundColor = '';
            urlError.textContent = '';
        } else if (!result.urlValid) {
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

        let isNameFilled = fullNameInput && fullNameInput.value.trim() !== '';
        let isPositionFilled = positionInput && positionInput.value.trim() !== '';
        let isDescFilled = descriptionInput && descriptionInput.value.trim() !== '';
        let isEmailFilled = emailInput && emailInput.value.trim() !== '' && emailInput.value.includes('@');
        let isPhoneFilled = phoneVal.trim() !== '';

        let areAllInputsFilled = isNameFilled && isPositionFilled && isDescFilled && isEmailFilled && isPhoneFilled;

        if (!areAllInputsFilled) {
            submitBtn.disabled = true;
            if (formWarning) {
                formWarning.style.color = 'red';
                formWarning.textContent = 'Please fill in all required fields (Name, Position, Description, Email, Phone).';
            }
        } else if (!result.allValid) {
            submitBtn.disabled = true;
            if (formWarning) {
                formWarning.style.color = 'red';
                formWarning.textContent = 'Please fix the invalid Phone or URL format!';
            }
        } else {
            submitBtn.disabled = false;
            if (formWarning) {
                formWarning.style.color = 'green';
                formWarning.textContent = '✓ All fields are correctly filled. Ready to add!';
            }
        }
    }

    if (employeeForm) {
        employeeForm.addEventListener('input', validateForm);
        validateForm(); 
    }

    renderTable();

    if (employeeForm) {
        employeeForm.addEventListener('submit', function (e) {
            e.preventDefault(); 
            showPreloader(); 

            let formData = new FormData(employeeForm);

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                hidePreloader(); 
                if (data.status === 'success') {
                    let newEmp = {
                        id: data.employee.id,
                        full_name: data.employee.full_name,
                        position: data.employee.position,
                        email: data.employee.email,
                        phone: data.employee.phone || 'N/A',
                        description: data.employee.description || 'No description',
                        photo: data.employee.photo ? data.employee.photo : null
                    };

                    tableData.push(newEmp);     
                    filteredData = [...tableData]; 
                    renderTable();              
                    employeeForm.reset();
                    validateForm();
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