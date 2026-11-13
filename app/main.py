from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


from .database import Base, engine, get_db
from .models import (
    Category,
    Product,
    Supplier,
    Warehouse,
    Client,
    PurchaseOrder,
    PurchaseOrderItem,
    SalesRecord,
    SalesRecordItem,
    StockMovement,
)
from .schemas import (
    CategoryCreate,CategoryResponse,
    ProductCreate,ProductUpdate,ProductResponse,
    SupplierCreate,SupplierResponse,
    WarehouseCreate,WarehouseResponse,
    ClientCreate,ClientResponse,
    PurchaseOrderCreate,PurchaseOrderResponse,
    PurchaseOrderItemCreate,PurchaseOrderItemResponse,
    SalesRecordCreate,SalesRecordResponse,
    SalesRecordItemCreate,SalesRecordItemResponse,
    StockMovementCreate,StockMovementResponse,
    InventoryBuyCreate,InventorySellCreate
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    version="1.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Inventory API is running"
    }

#create 

@app.post("/products",response_model=ProductResponse,status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    category = db.get(Category, product.category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_product = Product(
        name=product.name,
        category_id=product.category_id,
        price_sen=product.price_sen,
        quantity=product.quantity
    )


    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.post("/categories",response_model=CategoryResponse,status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Category)
        .filter(Category.name == category.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Category already exists"
        )

    new_category = Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.post("/suppliers",response_model=SupplierResponse,status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Supplier)
        .filter(Supplier.email == supplier.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Supplier email already exists"
        )

    new_supplier = Supplier(
        name=supplier.name,
        email=supplier.email,
        phone=supplier.phone
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier

@app.post("/warehouses",response_model=WarehouseResponse,status_code=201)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db)
):
    new_warehouse = Warehouse(
        name=warehouse.name,
        location=warehouse.location,
        state=warehouse.state
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse

@app.post("/clients",response_model=ClientResponse,status_code=201)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Client)
        .filter(Client.email == client.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Client email already exists"
        )

    new_client = Client(
        name=client.name,
        email=client.email,
        phone=client.phone
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client

@app.post("/purchase-orders",response_model=PurchaseOrderResponse,status_code=201)
def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    supplier = db.get(Supplier, purchase_order.supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    new_purchase_order = PurchaseOrder(
        supplier_id=purchase_order.supplier_id,
        order_date=purchase_order.order_date,
        status=purchase_order.status
    )

    db.add(new_purchase_order)
    db.commit()
    db.refresh(new_purchase_order)

    return new_purchase_order

@app.post("/purchase-order-items",response_model=PurchaseOrderItemResponse,status_code=201)
def create_purchase_order_item(
    item: PurchaseOrderItemCreate,
    db: Session = Depends(get_db)
):
    purchase_order = db.get(
        PurchaseOrder,
        item.purchase_order_id
    )

    if not purchase_order:
        raise HTTPException(
            status_code=404,
            detail="Purchase order not found"
        )

    product = db.get(Product, item.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing = (
        db.query(PurchaseOrderItem)
        .filter(
            PurchaseOrderItem.purchase_order_id
            == item.purchase_order_id,
            PurchaseOrderItem.product_id
            == item.product_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product already exists in this purchase order"
        )

    new_item = PurchaseOrderItem(
        purchase_order_id=item.purchase_order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        price_sen=item.price_sen
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@app.post("/sales-records",response_model=SalesRecordResponse,status_code=201)
def create_sales_record(
    sales_record: SalesRecordCreate,
    db: Session = Depends(get_db)
):
    client = db.get(Client, sales_record.client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    new_sales_record = SalesRecord(
        client_id=sales_record.client_id,
        status=sales_record.status
    )

    db.add(new_sales_record)
    db.commit()
    db.refresh(new_sales_record)

    return new_sales_record

@app.post("/sales-record-items",response_model=SalesRecordItemResponse,status_code=201)
def create_sales_record_item(
    item: SalesRecordItemCreate,
    db: Session = Depends(get_db)
):
    sales_record = db.get(
        SalesRecord,
        item.sales_record_id
    )

    if not sales_record:
        raise HTTPException(
            status_code=404,
            detail="Sales record not found"
        )

    product = db.get(Product, item.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing = (
        db.query(SalesRecordItem)
        .filter(
            SalesRecordItem.sales_record_id
            == item.sales_record_id,
            SalesRecordItem.product_id
            == item.product_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product already exists in this sales record"
        )

    new_item = SalesRecordItem(
        sales_record_id=item.sales_record_id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price_sen=item.unit_price_sen
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@app.post("/stock-movements",response_model=StockMovementResponse,status_code=201)
def create_stock_movement(
    movement: StockMovementCreate,
    db: Session = Depends(get_db)
):
    product = db.get(Product, movement.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if movement.source_warehouse_id:
        source_warehouse = db.get(
            Warehouse,
            movement.source_warehouse_id
        )

        if not source_warehouse:
            raise HTTPException(
                status_code=404,
                detail="Source warehouse not found"
            )

    if movement.destination_warehouse_id:
        destination_warehouse = db.get(
            Warehouse,
            movement.destination_warehouse_id
        )

        if not destination_warehouse:
            raise HTTPException(
                status_code=404,
                detail="Destination warehouse not found"
            )

    if movement.purchase_order_id:
        purchase_order = db.get(
            PurchaseOrder,
            movement.purchase_order_id
        )

        if not purchase_order:
            raise HTTPException(
                status_code=404,
                detail="Purchase order not found"
            )

    if movement.sales_record_id:
        sales_record = db.get(
            SalesRecord,
            movement.sales_record_id
        )

        if not sales_record:
            raise HTTPException(
                status_code=404,
                detail="Sales record not found"
            )

    new_movement = StockMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type=movement.movement_type,
        source_warehouse_id=movement.source_warehouse_id,
        destination_warehouse_id=movement.destination_warehouse_id,
        purchase_order_id=movement.purchase_order_id,
        sales_record_id=movement.sales_record_id
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement

# read all

@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()

@app.get("/clients", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.id).all()

@app.get("/suppliers", response_model=list[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).order_by(Supplier.id).all()
#read some 

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

# update 

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.quantity is not None:
        product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)

    return product

# delete

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }


# buybutton

@app.post("/inventory/buy", status_code=201)
def buy_inventory(
    data: InventoryBuyCreate,
    db: Session = Depends(get_db)
):
    # Check product
    product = db.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")


    # Check supplier
    supplier = db.get(Supplier, data.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404,detail="Supplier not found")        

    # Create Purchase Order

    purchase_order = PurchaseOrder(
        supplier_id=data.supplier_id,
        order_date=datetime.now(),
        status="completed"
    )

    db.add(purchase_order)

    # We need the generated PO ID
    db.flush()

    # Create Purchase Order Item

    purchase_item = PurchaseOrderItem(
        purchase_order_id=purchase_order.id,
        product_id=data.product_id,
        quantity=data.quantity,
        price_sen=data.price_sen
    )

    db.add(purchase_item)
    product.quantity += data.quantity


    # Create Stock Movement


    movement = StockMovement(
        product_id=data.product_id,
        quantity=data.quantity,
        movement_type="purchase",

        # Supplier -> Us
        source_warehouse_id=1,
        destination_warehouse_id=2,

        purchase_order_id=purchase_order.id
    )

    db.add(movement)

    db.commit()

    db.refresh(purchase_order)
    db.refresh(purchase_item)
    db.refresh(movement)
    db.refresh(product)

    return {
        "message": "Inventory purchased successfully",
        "purchase_order": purchase_order,
        "purchase_order_item": purchase_item,
        "stock_movement": movement,
        "product_quantity": product.quantity
    }

#sellbutton

@app.post("/inventory/sell", status_code=201)
def sell_inventory(
    data: InventorySellCreate,
    db: Session = Depends(get_db)
):
    # Check product
    product = db.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")


    # Check client
    client = db.get(Client, data.client_id)
    if not client:
        raise HTTPException(status_code=404,detail="Client not found")



    # Check available stock


    if product.quantity < data.quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Insufficient stock. "
                f"Available: {product.quantity}, "
                f"Requested: {data.quantity}"
            )
        )


    # Create Sales Record


    sales_record = SalesRecord(client_id=data.client_id, status="completed")
    db.add(sales_record)
    # Get generated sales record ID
    db.flush()

    # Create Sales Record Item


    sales_item = SalesRecordItem(
        sales_record_id=sales_record.id,
        product_id=data.product_id,
        quantity=data.quantity,
        unit_price_sen=data.unit_price_sen
    )
    db.add(sales_item)
    product.quantity -= data.quantity

    # Create Stock Movement

    movement = StockMovement(
        product_id=data.product_id,
        quantity=data.quantity,
        movement_type="sale",

        # Us -> Client
        source_warehouse_id=2,
        destination_warehouse_id=3,

        sales_record_id=sales_record.id
    )
    db.add(movement)

    db.commit()

    db.refresh(sales_record)
    db.refresh(sales_item)
    db.refresh(movement)
    db.refresh(product)

    return {
        "message": "Inventory sold successfully",
        "sales_record": sales_record,
        "sales_record_item": sales_item,
        "stock_movement": movement,
        "product_quantity": product.quantity
    }