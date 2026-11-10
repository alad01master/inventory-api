from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price_sen: int = Field(gt=0)
    quantity: int = Field(ge=0)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price_sen: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price_sen: int
    quantity: int

    model_config = {
        "from_attributes": True
    }