from models import db


class Unit(db.Model):
    """
    Model for the 'units' table.
    This table defines measurement units for products.
    """

    __tablename__ = "units"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )  # Unique identifier for each unit
    name = db.Column(db.String, nullable=False, unique=True)  # Name of the unit
    percentage_of_the_stock = db.Column(
        db.Numeric(precision=5, scale=2), nullable=True
    )  # Percentage of stock filled by this unit

    product = db.relationship(
        "Product", back_populates="unit", cascade="all", passive_deletes=True
    )  # Relationship to products

    def __repr__(self):
        """
        Provides a string representation of the Unit instance.
        """
        return f"<Unit(id={self.id}, name='{self.name}')>"