import pytest
import time
import re
from playwright.sync_api import Page, expect
from ui_tests.page_objects import CatalogPage, LoginPage


@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(page: Page, request):
    """Фикстура для сохранения скриншота при падении теста"""
    yield
    if request.node.rep_call.failed:
        import os

        os.makedirs("test-results", exist_ok=True)
        screenshot_path = f"test-results/{request.node.name}.png"
        page.screenshot(path=screenshot_path, full_page=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def test_catalog_opens_and_shows_books(page: Page):
    """Тест 1: Главная страница открывается и отображает сетку книг"""
    catalog = CatalogPage(page)
    catalog.navigate()

    expect(page).to_have_title(re.compile(r"Book", re.IGNORECASE))
    expect(catalog.book_cards.first).to_be_visible()


def test_theme_switcher_functionality(page: Page):
    """Тест 2: Переключение темы сайта (Dark/Light mode)"""
    catalog = CatalogPage(page)
    catalog.navigate()

    catalog.switch_theme()
    expect(catalog.body).to_have_class(re.compile("dark-theme"))


def test_login_invalid_user_ui(page: Page):
    """Тест 2: Негативный сценарий входа (ПАДАЮЩИЙ ТЕСТ ДЛЯ СКРИНШОТА)"""
    login_page = LoginPage(page)

    unique_username = f"fakeuser_{int(time.time())}"
    unique_password = "FakePassword123!"

    login_page.login(unique_username, unique_password)

    expect(page).to_have_title(re.compile(r"Book", re.IGNORECASE))
