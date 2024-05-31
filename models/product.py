from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    # TO-DO: BONUS: (1) view and manage stock levels, (2) restock products when low
    stock_quantity: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Product {self.id}|{self.name}>"