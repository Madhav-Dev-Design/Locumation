from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"},
    {"id": 3, "name": "Headphones"},
]
from itertools import cycle
product_cycle = cycle(products)

@app.get("/delayed")
async def delayed(id: int = None):
    if id is not None:
        product = next((p for p in products if p["id"] == id), None)
        if not product:
            raise HTTPException(404, "Product not found")
    else:
        product = next(product_cycle)
        id = product["id"]

    if id == 1:
        await asyncio.sleep(5)
    elif id == 2:
        await asyncio.sleep(10)
    else:
        await asyncio.sleep(0)
    return product

@app.get("/products")
async def get_products():
    return products

@app.get("/products/{pid}")
async def get_product(pid: int):
    product = next((p for p in products if p["id"] == pid), None)
    if product:
        return product
    raise HTTPException(404, "Product not found")

@app.post("/products")
async def add_product(request: Request):
    data = await request.json()
    if "name" not in data:
        raise HTTPException(400, "Name required")
    new_id = max(p["id"] for p in products) + 1
    new_product = {"id": new_id, "name": data["name"]}
    await asyncio.sleep(3)
    products.append(new_product)
    return new_product

@app.put("/products/{pid}")
async def update_product(pid: int, request: Request):
    data = await request.json()
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        raise HTTPException(404, "Product not found")
    if "name" in data:
        await asyncio.sleep(4)
        product["name"] = data["name"]
    return product

@app.delete("/products/{pid}")
async def delete_product(pid: int):
    global products
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        raise HTTPException(404, "Product not found")
    await asyncio.sleep(2)
    products = [p for p in products if p["id"] != pid]
    return {"status": "deleted"}