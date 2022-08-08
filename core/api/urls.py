from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.User.views_user import UserViewSet, Login, Logout
from core.api.Client.views_client import ClientViewSet
from core.api.Category.views_category import CategoryViewSet
from core.api.Product.views_product import ProductViewSet
from core.api.SaleDetail.views_sale_detail import SaleDetailViewSet
from core.api.Sale.views_cart import CartViewSet
from core.api.Sale.views_sale import SaleViewSet
from core.api.pedido.view_pedido import PedidoViewSet


router = DefaultRouter()

router.register(r'UsersApi', UserViewSet, basename='UsersApi')
router.register(r'Client', ClientViewSet, basename='Client')
router.register(r'Category', CategoryViewSet, basename='Category')
router.register(r'Product', ProductViewSet, basename='Product')
router.register(r'Sale', SaleViewSet, basename='Sale')
router.register(r'Pedidos', PedidoViewSet, basename='Pedidos')
router.register(r'SaleDetail', SaleDetailViewSet, basename='SaleDetail')
router.register(r'Cart', CartViewSet, basename='Cart')

urlpatterns = [
    path('', include(router.urls), name="ViewApi"),
    path('Login/', Login.as_view(), name="Login"),
    path('Logout/', Logout.as_view(), name="Logout"),
]