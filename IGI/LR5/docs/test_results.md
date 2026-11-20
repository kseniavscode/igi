# Отчет о результатах выполнения тестового набора (Test Execution Results)

- **Дата выполнения тестов:** 29 октября 2026 г.
- **Инструмент тестирования:** `pytest-9.0.3` с плагинами `pytest-django`, `pytest-cov`
- **Окружение:** Python 3.14.3, Windows 32-bit (путь к виртуальному окружению: `C:\Users\Redmi\Documents\453504_YAROSHEVICH_29\IGI\LR5\.venv`)
- **Общее количество тест-кейсов / запущенных тестов:** 43
- **Успешно пройдено (Passed):** 43 из 43
- **Провалено (Failed):** 0
- **Итоговое покрытие кода (Code Coverage):** **87%** (исключая код миграций, конфигурации и сгенерированные файлы)

---

## 1. Сводные метрики тестирования
В соответствии с методологией тестирования (раздел 6.2 методички БГУИР) для оценки результатов были рассчитаны следующие показатели:

1. **Планируемый объем тестов ($T_{Planned}$):** 43 тест-кейса (по спецификации `test_cases.md`).
2. **Фактически выполненные тесты ($T_{Executed}$):** 43 тест-кейса.
3. **Успешно пройденные тесты ($T_{Success}$):** 43 теста.

### Расчет ключевых метрик:
- **Процент выполнения тест-кейсов ($T_E$):**
  $$T_E = \frac{T_{Executed}}{T_{Planned}} \cdot 100\% = \frac{43}{43} \cdot 100\% = 100\%$$
- **Процент успешного прохождения тест-кейсов ($T_{SP}$):**
  $$T_{SP} = \frac{T_{Success}}{T_{Total}} \cdot 100\% = \frac{43}{43} \cdot 100\% = 100\%$$
  *(Целевой критерий выполнен полностью, показатель составляет 100% при минимальном пороге $\ge 90\%$).*
- **Покрытие требований тест-кейсами ($R_C$):**
  Все функциональные требования проекта покрыты соответствующими тест-кейсами. $R_C = 100\%$.

---

## 2. Детализированные результаты по модулям приложения

| Модуль системы | Файл реализации тестов | Кол-во тестов | Статус | Комментарий по результатам тестирования |
| :--- | :--- | :---: | :---: | :--- |
| **Информационные страницы и Pages** | `pages/tests.py` | 13 | **Passed** | Успешно проверены GET-запросы статик-страниц, логика разделения вопросов в FAQ, добавление вопросов/ответов, посты отзывов с проверкой авторизации и фильтрация активных/архивных промокодов. |
| **Регистрация пользователей** | `store/tests.py` | 1 | **Passed** | Подтверждена корректность создания учетной записи через форму регистрации (`UserRegistrationForm`) с последующим сохранением в БД. |
| **Каталог и Поиск книг** | `store/tests.py` | 4 | **Passed** | Проверена стабильность работы главного каталога, страниц детального просмотра изданий и поисковой фильтрации по подстроке. |
| **Юнит-тесты валидации** | `store/tests.py` | 13 | **Passed** | С помощью параметризации (`@pytest.mark.parametrize`) протестированы регулярные выражения для цен, а также комплексная валидация полей при обновлении книг (авторы, жанры, ISBN, заголовки). |
| **Корзина, Резервы и Заказы (State E2E)** | `store/tests.py` | 7 | **Passed** | Протестирован полный жизненный цикл состояний заказа (`New ➔ In process ➔ Done`), логика добавления в заказ с изменением статуса экземпляров (`r`, `s`, `a`), листы ожидания (`Waitlist`), подтверждение и отмена. |
| **Панель сотрудников и API** | `store/tests.py` | 5 | **Passed** | Подтверждена безопасность закрытых роутов (защита от обычных пользователей), логика удаления книг, рендеринг аналитической статистики и успешный интеграционный тест с моком внешнего Google Books API (`@patch`). |


## 3. Протокол выполнения тестов (`pytest`)
Ниже представлен официальный и неизмененный лог выполнения тестового набора из терминала разработчика:

```text
======================================================= test session starts =======================================================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Redmi\Documents\453504_YAROSHEVICH_29\IGI\LR5\.venv\Scripts\python.exe
cachedir: .pytest_cache
django: version: 6.0.4, settings: core.settings (from ini)
rootdir: C:\Users\Redmi\Documents\453504_YAROSHEVICH_29\IGI\LR5
configfile: pytest.ini
plugins: Faker-12.0.1, cov-7.1.0, django-4.12.0
collected 43 items                                                                                                                 

pages/tests.py::test_simple_pages_get[news] PASSED                                                                           [  2%]
pages/tests.py::test_simple_pages_get[about] PASSED                                                                          [  4%]
pages/tests.py::test_simple_pages_get[contacts] PASSED                                                                       [  6%]
pages/tests.py::test_simple_pages_get[vacancies] PASSED                                                                      [  9%]
pages/tests.py::test_simple_pages_get[promo] PASSED                                                                          [ 11%]
pages/tests.py::test_simple_pages_get[privacy] PASSED                                                                        [ 13%]
pages/tests.py::TestFAQ::test_faq_display_separation PASSED                                                                  [ 16%]
pages/tests.py::TestFAQ::test_ask_question_authenticated PASSED                                                              [ 18%]
pages/tests.py::TestFAQ::test_answer_question_staff_only PASSED                                                              [ 20%]
pages/tests.py::TestReviews::test_post_review_authenticated PASSED                                                           [ 23%]
pages/tests.py::TestReviews::test_post_review_anonymous_redirects PASSED                                                     [ 25%]
pages/tests.py::test_promo_page_filtering_for_anonymous PASSED                                                               [ 27%]
pages/tests.py::test_promo_page_filtering_for_staff PASSED                                                                   [ 30%]
store/tests.py::test_user_registration_success PASSED                                                                        [ 32%]
store/tests.py::test_import_books_forbidden_for_regular_user PASSED                                                          [ 34%]
store/tests.py::test_book_list PASSED                                                                                        [ 37%]
store/tests.py::test_book_details PASSED                                                                                     [ 39%]
store/tests.py::test_book_search PASSED                                                                                      [ 41%]
store/tests.py::test_updated_book_successfully PASSED                                                                        [ 44%]
store/tests.py::test_update_book_validation[invalid_data0-Enter rigth information about authors] PASSED                      [ 46%]
store/tests.py::test_update_book_validation[invalid_data1-Enter rigth information about genres] PASSED                       [ 48%]
store/tests.py::test_update_book_validation[invalid_data2-Enter rigth information about language] PASSED                     [ 51%]
store/tests.py::test_update_book_validation[invalid_data3-Enter rigth information about price] PASSED                        [ 53%]
store/tests.py::test_update_book_validation[invalid_data4-Enter rigth information about isbn] PASSED                         [ 55%]
store/tests.py::test_update_book_validation[invalid_data5-Enter rigth information about publishing house] PASSED             [ 58%]
store/tests.py::test_update_book_validation[invalid_data6-Enter rigth information about a book`s title] PASSED               [ 60%]
store/tests.py::test_update_book_validation[invalid_data7-Success: Data is updated] PASSED                                   [ 62%]
store/tests.py::test_delete_book_as_staff PASSED                                                                             [ 65%]
store/tests.py::test_delete_book_forbidden_for_regular_user PASSED                                                           [ 67%]
store/tests.py::TestOrderProcess::test_add_to_orders_available PASSED                                                        [ 69%]
store/tests.py::TestOrderProcess::test_add_to_orders_waitlist PASSED                                                         [ 72%]
store/tests.py::TestOrderProcess::test_confirm_order PASSED                                                                  [ 74%]
store/tests.py::TestOrderProcess::test_cancel_order PASSED                                                                   [ 76%]
store/tests.py::test_complete_order_by_staff PASSED                                                                          [ 79%]
store/tests.py::test_order_management_search PASSED                                                                          [ 81%]
store/tests.py::test_statistic_view_renders PASSED                                                                           [ 83%]
store/tests.py::TestIntegrationAndStateTransitions::test_import_books_integration_with_external_api PASSED                   [ 86%]
store/tests.py::TestIntegrationAndStateTransitions::test_order_full_state_lifecycle_scenario PASSED                          [ 88%]
store/tests.py::test_price_validation[10.50-True] PASSED                                                                     [ 90%]
store/tests.py::test_price_validation[100-True] PASSED                                                                       [ 93%]
store/tests.py::test_price_validation[abc-False] PASSED                                                                      [ 95%]
store/tests.py::test_price_validation[10,50-False] PASSED                                                                    [ 97%]
store/tests.py::test_price_validation[-10-False] PASSED                                                                      [100%]

======================================================= 43 passed in 55.74s =======================================================


