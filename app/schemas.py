from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime

#create schemas for the models

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category_id: int
    price_sen: int = Field(ge=0)
    quantity: int = Field(ge=0)

class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=20)

class WarehouseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=255)
    state: str = Field(min_length=1, max_length=50)

class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=20)

class PurchaseOrderCreate(BaseModel):
    supplier_id: int = Field(gt=0)
    order_date: datetime
    status: str = Field(
        default="pending",
        pattern="^(pending|completed|cancelled)$"
    )

class PurchaseOrderItemCreate(BaseModel):
    purchase_order_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    price_sen: int = Field(ge=0)

class SalesRecordCreate(BaseModel):
    client_id: int = Field(gt=0)
    status: str = Field(
        default="pending",
        pattern="^(pending|completed|cancelled)$"
    )

class SalesRecordItemCreate(BaseModel):
    sales_record_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price_sen: int = Field(ge=0)

class StockMovementCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

    movement_type: str = Field(
        pattern="^(purchase|sale|transfer|adjustment)$"
    )

    source_warehouse_id: int | None = Field(default=None, gt=0)
    destination_warehouse_id: int | None = Field(default=None, gt=0)

    purchase_order_id: int | None = Field(default=None, gt=0)
    sales_record_id: int | None = Field(default=None, gt=0)

#update schemas for the models
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price_sen: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)



#response schemas for the models
class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CategoryResponse(ORMResponse):
    id: int
    code: str
    name: str
    created_at: datetime
    updated_at: datetime

class ProductResponse(ORMResponse):
    id: int
    code: str
    name: str
    category_id: int
    price_sen: int
    quantity: int
    created_at: datetime
    updated_at: datetime

class SupplierResponse(ORMResponse):
    id: int
    code: str
    name: str
    email: str
    phone: str | None
    created_at: datetime
    updated_at: datetime

class WarehouseResponse(ORMResponse):
    id: int
    code: str
    name: str
    location: str
    state: str
    created_at: datetime
    updated_at: datetime

class ClientResponse(ORMResponse):
    id: int
    code: str
    name: str
    email: str
    phone: str | None
    created_at: datetime
    updated_at: datetime

class PurchaseOrderResponse(ORMResponse):
    id: int
    code: str
    supplier_id: int
    order_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

class PurchaseOrderItemResponse(ORMResponse):
    id: int
    purchase_order_id: int
    product_id: int
    quantity: int
    price_sen: int
    created_at: datetime
    updated_at: datetime

class SalesRecordResponse(ORMResponse):
    id: int
    code: str
    client_id: int
    status: str
    created_at: datetime
    updated_at: datetime

class SalesRecordItemResponse(ORMResponse):
    id: int
    sales_record_id: int
    product_id: int
    quantity: int
    unit_price_sen: int
    created_at: datetime

class StockMovementResponse(ORMResponse):
    id: int
    code: str
    product_id: int
    quantity: int
    movement_type: str
    source_warehouse_id: int | None
    destination_warehouse_id: int | None
    purchase_order_id: int | None
    sales_record_id: int | None
    created_at: datetime

#button
class InventoryBuyCreate(BaseModel):
    product_id: int = Field(gt=0)
    supplier_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    price_sen: int = Field(ge=0)


class InventorySellCreate(BaseModel):
    product_id: int = Field(gt=0)
    client_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price_sen: int = Field(ge=0)