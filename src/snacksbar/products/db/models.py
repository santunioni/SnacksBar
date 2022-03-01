from __future__ import annotations
from decimal import Decimal
from typing import List, Union

import sqlalchemy as sql
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship, Session

from snacksbar.products.routes.dtos import Identified

Base: DeclarativeMeta = declarative_base()

snacks_have_ingredients = sql.Table(
    "snacks_have_ingredients",
    Base.metadata,
    sql.Column("snack_id", sql.Integer, sql.ForeignKey("snack.id"), nullable=False),
    sql.Column(
        "ingredient_id", sql.Integer, sql.ForeignKey("ingredient.id"), nullable=False
    ),
)


class Snack(Base):
    __tablename__ = "snack"
    id: int = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name: str = sql.Column(sql.String, nullable=False)
    category_id: int = sql.Column(
        sql.Integer, sql.ForeignKey("category.id"), nullable=True
    )
    category: Category = relationship("Category", back_populates="snacks")
    ingredients: List[Ingredient] = relationship(
        "Ingredient", secondary=snacks_have_ingredients, back_populates="snacks"
    )

    @property
    def __session(self) -> Session:
        return self._sa_instance_state.session

    def insert_ingredient(self, ingredient: Union[Ingredient, Identified]):
        if not isinstance(ingredient, Ingredient):
            ingredient = self.__session.query(Ingredient).get(ingredient.id)
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)


class Category(Base):
    __tablename__ = "category"
    id: int = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name: str = sql.Column(sql.String, nullable=False)
    price: Decimal = sql.Column(sql.DECIMAL, nullable=False)
    snacks: List[Snack] = relationship("Snack", back_populates="category")


class Ingredient(Base):
    __tablename__ = "ingredient"
    id: int = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name: str = sql.Column(sql.String, nullable=False)
    price: Decimal = sql.Column(sql.DECIMAL, nullable=False)
    snacks: List[Snack] = relationship(
        "Snack", secondary=snacks_have_ingredients, back_populates="ingredients"
    )


class Drink(Base):
    __tablename__ = "drink"
    id: int = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name: str = sql.Column(sql.String, nullable=False)
    price: Decimal = sql.Column(sql.DECIMAL, nullable=False)
