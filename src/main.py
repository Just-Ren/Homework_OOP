from typing import Any
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def __str__(self):
        pass

class MixinPrint:
    """Класс миксин для вывода в консоль информацию об объекте"""

    def __init__(self):
        print(repr(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class BaseProduct(ABC):
    """Абстрактный класс для всех продуктов"""

    @classmethod
    @abstractmethod
    def new_product(cls, *args, **kwargs):
        pass


class Product(BaseProduct, MixinPrint):
    """Продукт"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(other) is Product:
            return self.quantity * self.price + other.quantity * other.price
        raise TypeError

    @classmethod
    def new_product(cls, new_product: dict):
        """Взвращает созданный объект класса Product из параметров товара в словаре"""
        name = new_product["name"]
        description = new_product["description"]
        price = new_product["price"]
        quantity = new_product["quantity"]
        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


class Category(Base):
    """Категория товара"""

    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)
        print(Category.product_count)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."

    def add_product(self, product: Product) -> Any:
        if isinstance(product, Product):
            try:
                if product.quantity == 0:
                    raise ZeroProductException(
                        "Нельзя добавить товар с нулевым количеством"
                    )
            except ZeroProductException as e:
                print(str(e))
            else:
                self.__products.append(product)
                Category.product_count += 1
                print("Товар успешно добавлен")
            finally:
                print("Обработка добавления товара завершена")
        else:
            raise TypeError

    @property
    def get_product_list(self) -> str:
        product_list = ""
        for product in self.__products:
            product_list += f"{str(product)}\n"
        return product_list

    @property
    def products(self) -> list:
        products_list = []
        for product in self.__products:
            products_list.append(product)
        return products_list

    def middle_price(self):
        try:
            return sum(product.price for product in self.__products) / len(
                self.__products
            )
        except ZeroDivisionError:
            return 0

    @property
    def get_product_list(self) -> str:
        product_list = ""
        for product in self.__products:
            product_list += f"{str(product)}\n"
        return product_list

    @property
    def products(self) -> list:
        products_list = []
        for product in self.__products:
            products_list.append(product)
        return products_list


# result = Category("Product", "Description", ["product1", "product2", "product3"])
# print(result)

class ProductIterator:
    """Класс для итерации товаров одной категории"""

    def __init__(self, category_obj):
        self.category = category_obj
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category.products):
            prod = self.category.products[self.index]
            self.index += 1
            return prod
        else:
            raise StopIteration

class Smartphone(Product):
    """Товары категории Сматрфоны"""

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        if type(other) is Smartphone:
            return self.quantity * self.price + other.quantity * other.price
        raise TypeError

class LawnGrass(Product):
    """Товары категории Газонная трава"""

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        if type(other) is LawnGrass:
            return self.quantity * self.price + other.quantity * other.price
        raise TypeError

class Order(Base):
    product: str
    quantity: int
    total_price: float

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total_price = self.get_total_price()

    def __str__(self):
        return f"Ваш заказ: {self.product.name}, {self.quantity} шт. на сумму {self.total_price} руб."

    def get_total_price(self):
        price = product.price
        total_price = price * self.quantity
        return total_price

class ZeroProductException(Exception):

    def __init__(self, message=None):
        super.__init__(message)


if __name__ == "__main__":
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством"
        )
    else:
        print(
            "Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством"
        )

    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны", "Категория смартфонов", [product1, product2, product3]
    )

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
