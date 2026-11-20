from locust import HttpUser, task, between


class BookstoreUser(HttpUser):
    wait_time = between(1, 5)

    @task(7)  # 70% времени
    def view_catalog(self):
        self.client.get("/")

    @task(2)  # 20% времени
    def search(self):
        self.client.get("/?search=Python")

    @task(1)  # 10% времени
    def add_to_cart(self):
        self.client.get("/add-to-orders/2/")
