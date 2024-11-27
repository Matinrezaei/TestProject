from rest_framework import generics
from .models import Product, Category, Cart
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer
from .Permisions import IsAdminOrReadOnly


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryProductsView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)

            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')
            stock = request.data.get('stock')

            if not name or not price:
                return Response({"error": "name and price are required"}, status=400)

            new_product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                views=0,
                category=category,
                stock=stock,
            )

            return Response({"message": "Product added to category successfully", "product_id": new_product.id}, status=201)
        
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AddToCartView(APIView):
    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            cart, created = Cart.objects.get_or_create(id=1)
            cart.products.add(product)
            return Response({"message": "Product added to cart"})
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

class RemoveFromCartView(APIView):
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            cart = Cart.objects.get(id=1)
            cart.products.remove(product)
            return Response({"message": "Product removed from cart"})
        except (Product.DoesNotExist, Cart.DoesNotExist):
            return Response({"error": "Product or Cart not found"}, status=404)

class ViewCartView(APIView):
    def get(self, request):
        try:
            cart = Cart.objects.get(id=1)
            products = cart.products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"error": "no product"}, status=404)

class ClearCartView(APIView):
    def delete(self, request):
        try:
            cart = Cart.objects.get(id=1)
            cart.products.clear()
            return Response({"message": "Cart cleared"})
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

