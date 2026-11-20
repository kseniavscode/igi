from playwright.sync_api import Page


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://igi-kvbf.onrender.com"

    def navigate(self, path: str = ""):
        self.page.goto(f"{self.base_url}/{path}")


class CatalogPage(BasePage):
    """Страница каталога книг"""

    def __init__(self, page: Page):
        super().__init__(page)

        self.search_input = page.locator("input[name='search']")
        self.search_button = page.locator("form.search_form button[type='submit']")
        self.book_cards = page.locator(".book_card")
        self.theme_btn = page.locator("#theme_toggle")
        self.body = page.locator("body")

    def search_for_book(self, query: str):
        self.search_input.fill(query)
        self.search_button.click()

    def switch_theme(self):
        self.theme_btn.click()


class LoginPage(BasePage):
    """Страница авторизации"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_btn = page.locator("button[type='submit']")
        self.error_message = page.locator(".class_messages")

    def login(self, username: str, password: str):
        self.navigate("login/")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
