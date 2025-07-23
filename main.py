"""FastAPI application for Product CRUD operations."""
from typing import List
import uvicorn

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

from models import Product, ProductCreate, ProductUpdate
from database import db

app = FastAPI(
    title="Product CRUD API",
    description="A simple CRUD API for managing products",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Root endpoint returning the main frontend page."""
    products = db.get_all_products()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api")
def api_root():
    """API root endpoint returning welcome message."""
    return {"message": "Welcome to the Product CRUD API"}


@app.get("/products", response_model=List[Product])
def get_products():
    """Get all products"""
    return db.get_all_products()


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Get a specific product by ID"""
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    """Create a new product"""
    # TODO: Add validation logic here
    return db.create_product(product)


@app.post("/products/create")
async def create_product_form(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    tags: str = Form(""),
    in_stock: bool = Form(True)
):
    """Create a new product from form data"""
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    
    product_data = ProductCreate(
        name=name,
        description=description,
        price=price,
        category=category,
        tags=tag_list,
        in_stock=in_stock
    )
    
    db.create_product(product_data)
    return RedirectResponse(url="/", status_code=303)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    """Update an existing product"""
    # TODO: Add validation and error handling
    updated_product = db.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.post("/products/{product_id}/update")
async def update_product_form(
    request: Request,
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    tags: str = Form(""),
    in_stock: bool = Form(True)
):
    """Update an existing product from form data"""
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    
    product_update = ProductUpdate(
        name=name,
        description=description,
        price=price,
        category=category,
        tags=tag_list,
        in_stock=in_stock
    )
    
    updated_product = db.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return RedirectResponse(url="/", status_code=303)


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product"""
    # TODO: Add proper response handling
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@app.post("/products/{product_id}/delete")
async def delete_product_form(request: Request, product_id: int):
    """Delete a product from form submission"""
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return RedirectResponse(url="/", status_code=303)


@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_page(request: Request, product_id: int):
    """Edit product page"""
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("edit.html", {"request": request, "product": product})


@app.get("/products/new", response_class=HTMLResponse)
def new_product_page(request: Request):
    """New product page"""
    return templates.TemplateResponse("new.html", {"request": request})


# TODO: Add search endpoint with AI-powered features
# @app.get("/products/search")
# def search_products(query: str):
#     """Search products using AI-powered search"""
#     pass

# TODO: Add product recommendations endpoint
# @app.get("/products/{product_id}/recommendations")
# def get_product_recommendations(product_id: int):
#     """Get AI-powered product recommendations"""
#     pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
