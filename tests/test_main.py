import pytest

from src.main import Category, Product

@pytest.fixture
def first_product():
    return Product(
        name="Product",
        description="Description of the product",
        price=84.50,
        quantity=10,
    )


@pytest.fixture
def second_product():
    return Product(
        name="Product number two",
        description="Description of the product number two",
        price=155.87,
        quantity=34,
    )


@pytest.fixture
def first_category():
    return Category(
        name="Category",
        description="Description of the category",
        products=[
            Product(
                name="Product",
                description="Description of the product",
                price=84.50,
                quantity=10,
            ),
            Product(
                name="Product number two",
                description="Description of the product number two",
                price=155.87,
                quantity=34,
            ),
        ],
    )


@pytest.fixture
def second_category():
    return Category(
        name="Category number two",
        description="Description of the category number two",
        products=[
            Product(
                name="Product",
                description="Description of the product",
                price=84.50,
                quantity=10,
            ),
            Product(
                name="Product number two",
                description="Description of the product number two",
                price=155.87,
                quantity=34,
            ),
            Product(
                name="Product three",
                description="Description of the product three",
                price=8467.56,
                quantity=32,
            ),
        ],
    )


@pytest.fixture
def product_dict():
    return {
        "name": "Product 4",
        "description": "Description of the product 4",
        "price": 145.75,
        "quantity": 23,
    }

def test_category(first_category, second_category):
    assert first_category.name == "Category"
    assert first_category.description == "Description of the category"
    assert (
        first_category.get_product_list
        == "Product, 84.5 руб. Остаток: 10 шт.\nProduct number two, 155.87 руб. Остаток: 34 шт.\n"
    )

    assert first_category.category_count == 2
    assert second_category.category_count == 2

    assert first_category.product_count == 5
    assert second_category.product_count == 5


def test_cat_get_product_list_property(first_category, second_category):
    with pytest.raises(AttributeError):
        print(first_category.__products)
    assert (
        first_category.get_product_list
        == "Product, 84.5 руб. Остаток: 10 шт.\nProduct number two, 155.87 руб. Остаток: 34 шт.\n"
    )
    assert (
        second_category.get_product_list
        == "Product, 84.5 руб. Остаток: 10 шт.\nProduct number two, 155.87 руб. Остаток: 34 шт."
        "\nProduct three, 8467.56 руб. Остаток: 32 шт.\n"
    )


def test_category_str(first_category, second_category):
    assert str(first_category) == "Category, количество продуктов: 2 шт."
    assert str(second_category) == "Category number two, количество продуктов: 3 шт."

def test_product(first_product, second_product):
    assert first_product.name == "Product"
    assert first_product.description == "Description of the product"
    assert first_product.price == 84.50
    assert first_product.quantity == 10

    assert second_product.name == "Product number two"
    assert second_product.description == "Description of the product number two"
    assert second_product.price == 155.87
    assert second_product.quantity == 34


def test_new_product(product_dict):
    product4 = Product.new_product(product_dict)
    assert product4.name == "Product 4"
    assert product4.description == "Description of the product 4"
    assert product4.price == 145.75
    assert product4.quantity == 23


def test_prod_price_property(capsys, first_product):
    first_product.price = -756.57
    message = capsys.readouterr()
    assert message.out.strip() == "Цена не должна быть нулевая или орицательная"
    first_product.price = 756.57
    assert first_product.price == 756.57


def test_product_str(first_product):
    assert str(first_product) == "Product, 84.5 руб. Остаток: 10 шт."


def test_product_add(first_product, second_product):
    assert first_product + second_product == 6144.58
