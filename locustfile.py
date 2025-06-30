from locust import HttpUser, task, between
import random

class PerfTest(HttpUser):
    wait_time = between(1, 2)
    created_product_ids = []

    @task(2)
    def get_delayed(self):
        for i in [1, 2, 3]:
            if i not in self.created_product_ids:
                self.client.get(f"/delayed?id={i}")

    @task(3)
    def get_products(self):
        self.client.get("/products")

    @task(1)
    def get_product(self):
        if self.created_product_ids:
            pid = random.choice(self.created_product_ids)
            self.client.get(f"/products/{pid}")

    @task(2)
    def create_product(self):
        name = f"Test{random.randint(100,999)}"
        response = self.client.post("/products", json={"name": name})
        if response.status_code == 200 or response.status_code == 201:
            try:
                pid = response.json().get("id")
                if pid and pid not in self.created_product_ids:
                    self.created_product_ids.append(pid)
            except Exception:
                pass

    @task(1)
    def update_product(self):
        if self.created_product_ids:
            pid = random.choice(self.created_product_ids)
            self.client.put(f"/products/{pid}", json={"name": f"Updated{random.randint(1,1000)}"})

    @task(1)
    def delete_product(self):
        if self.created_product_ids:
            pid = self.created_product_ids.pop(0)
            self.client.delete(f"/products/{pid}")