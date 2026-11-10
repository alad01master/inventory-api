from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Category(Base):
    __tablename__ = "category"

    __table_args__ = (
        UniqueConstraint("code", name="uq_category_code"),
        UniqueConstraint("name", name="uq_category_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('CAT' || lpad(nextval('cat_seq'::regclass)::text, 3, '0'))"
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )

class Product(Base):
    __tablename__ = "product"

    __table_args__ = (
        UniqueConstraint("code", name="uq_product_code"),
        CheckConstraint("price_sen >= 0", name="ck_product_price_nonnegative"),
        CheckConstraint("quantity >= 0", name="ck_product_quantity_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('P' || lpad(nextval('p_seq'::regclass)::text, 3, '0'))"
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    price_sen: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    category: Mapped["Category"] = relationship(
        back_populates="products"
    )

    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="product"
    )

    purchase_order_items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="product"
    )

    sales_record_items: Mapped[list["SalesRecordItem"]] = relationship(
        back_populates="product"
    )

class Supplier(Base):
    __tablename__ = "supplier"

    __table_args__ = (
        UniqueConstraint("code", name="uq_supplier_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('S' || lpad(nextval('s_seq'::regclass)::text, 3, '0'))"
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="supplier"
    )

class Warehouse(Base):
    __tablename__ = "warehouse"

    __table_args__ = (
        UniqueConstraint("code", name="uq_warehouse_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('WH' || lpad(nextval('wh_seq'::regclass)::text, 3, '0'))"
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    outgoing_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="source_warehouse",
        foreign_keys="StockMovement.source_warehouse_id",
    )

    incoming_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="destination_warehouse",
        foreign_keys="StockMovement.destination_warehouse_id",
    )

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    __table_args__ = (
        UniqueConstraint("code", name="uq_purchase_order_code"),
        CheckConstraint(
            "status IN ('pending', 'completed', 'cancelled')",
            name="ck_purchase_order_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('PO' || lpad(nextval('po_seq'::regclass)::text, 3, '0'))"
        ),
    )

    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    supplier: Mapped["Supplier"] = relationship(
        back_populates="purchase_orders"
    )

    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )

    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="purchase_order"
    )

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_item"

    __table_args__ = (
        UniqueConstraint(
            "purchase_order_id",
            "product_id",
            name="uq_purchase_order_item",
        ),
        CheckConstraint("quantity > 0", name="ck_po_item_quantity_positive"),
        CheckConstraint("price_sen >= 0", name="ck_po_item_price_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("purchase_order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_sen: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="items"
    )

    product: Mapped["Product"] = relationship(
        back_populates="purchase_order_items"
    )

class Client(Base):
    __tablename__ = "client"

    __table_args__ = (
        UniqueConstraint("code", name="uq_client_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('C' || lpad(nextval('c_seq'::regclass)::text, 3, '0'))"
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    sales_records: Mapped[list["SalesRecord"]] = relationship(
        back_populates="client"
    )

class SalesRecord(Base):
    __tablename__ = "sales_record"

    __table_args__ = (
        UniqueConstraint("code", name="uq_sales_record_code"),
        CheckConstraint(
            "status IN ('pending', 'completed', 'cancelled')",
            name="ck_sales_record_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('SR' || lpad(nextval('sr_seq'::regclass)::text, 3, '0'))"
        ),
    )

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    client: Mapped["Client"] = relationship(
        back_populates="sales_records"
    )

    items: Mapped[list["SalesRecordItem"]] = relationship(
        back_populates="sales_record",
        cascade="all, delete-orphan",
    )

    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="sales_record"
    )

class SalesRecordItem(Base):
    __tablename__ = "sales_record_item"

    __table_args__ = (
        UniqueConstraint(
            "sales_record_id",
            "product_id",
            name="uq_sales_record_item",
        ),
        CheckConstraint("quantity > 0", name="ck_sales_item_quantity_positive"),
        CheckConstraint("unit_price_sen >= 0", name="ck_sales_item_price_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sales_record_id: Mapped[int] = mapped_column(ForeignKey("sales_record.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price_sen: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    sales_record: Mapped["SalesRecord"] = relationship(
        back_populates="items"
    )

    product: Mapped["Product"] = relationship(
        back_populates="sales_record_items"
    )

class StockMovement(Base):
    __tablename__ = "stock_movement"

    __table_args__ = (
        UniqueConstraint("code", name="uq_stock_movement_code"),
        CheckConstraint("quantity > 0", name="ck_stock_movement_quantity_positive"),
        CheckConstraint(
            "movement_type IN ('purchase', 'sale', 'transfer', 'adjustment')",
            name="ck_stock_movement_type",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text(
            "('SM' || lpad(nextval('sm_seq'::regclass)::text, 3, '0'))"
        ),
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    movement_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouse.id"), nullable=True)
    destination_warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouse.id"), nullable=True)
    destination_warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouse.id"), nullable=True)
    purchase_order_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_order.id"), nullable=True)
    sales_record_id: Mapped[int | None] = mapped_column(ForeignKey("sales_record.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    product: Mapped["Product"] = relationship(
        back_populates="stock_movements"
    )

    source_warehouse: Mapped["Warehouse"] = relationship(
        back_populates="outgoing_movements",
        foreign_keys=[source_warehouse_id],
    )

    destination_warehouse: Mapped["Warehouse"] = relationship(
        back_populates="incoming_movements",
        foreign_keys=[destination_warehouse_id],
    )

    purchase_order: Mapped["PurchaseOrder | None"] = relationship(
        back_populates="stock_movements"
    )

    sales_record: Mapped["SalesRecord | None"] = relationship(
        back_populates="stock_movements"
    )
