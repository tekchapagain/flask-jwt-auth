from flask_restful import Api
from resources.user import *
from resources.product import Product, ProductList
from resources.category import Category, CategoryList


def create_authentication_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    """
    'User API URL'
    api.add_resource(SignUpApi, "/api/auth/register")
    api.add_resource(LoginApi, "/api/auth/login")
    api.add_resource(WhoAmI, "/api/auth/whoami")
    api.add_resource(RefreshApi, "/api/auth/refresh")
    api.add_resource(LogoutApi, "/api/auth/logout")
    api.add_resource(ForgotPassword, "/api/auth/forgot")
    api.add_resource(ResetPassword, "/api/auth/reset-password")
    api.add_resource(ResetEmail, "/api/auth/emailreset")
    api.add_resource(UserListApi, "/api/auth/users")

    api.add_resource(ContactApi, "/api/contact")

    # api.add_namespace(product_ns)
    # api.add_namespace(products_ns)
    # api.add_namespace(category_ns)
    # api.add_namespace(categories_ns)

    api.add_resource(Product,'/api/product/<int:id>')
    api.add_resource(ProductList, "/api/products")
    api.add_resource(Category, '/api/category','/api/category/<int:id>')
    api.add_resource(CategoryList, "/api/categories")
