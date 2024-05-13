from cart.models import Cart, CartItem
from cart.views import add_to_cart
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from product.models import Category, Product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# from django.core.paginator import Paginator


class BaseView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class BlogPageView(TemplateView):
    template_name = "blog.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class ProductPageView(ListView):
    model = Product
    context_object_name = "products"
    queryset = Product.objects.all()
    # paginate_by = 10
    template_name = "products.html"

    # def get_queryset(self):
    #     return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_product_detail(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        context = {"product": product, "product_id": product_id}
        return context

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        product = self.object

        related_products = Product.objects.filter(
            category_id=product.category_id
        ).exclude(id=product.id)[:4]
        context["related_products"] = related_products

        similar_products = Product.objects.all()[:8]
        context["similar_products"] = similar_products
        return context


class CategoryPageView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category.html"


class CategoryDetailPageView(ListView):
    model = Category
    context_object_name = "category"
    template_name = "category_detail.html"

    def get_queryset(self):
        # Retrieve the category object based on the provided pk
        category_id = self.kwargs["pk"]
        return Category.objects.filter(pk=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add associated products to the context
        category = context["category"].first()  # Assuming there's only one category
        context["products"] = category.products.all()
        return context


class CartPageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CartItem
    context_object_name = "cart_items"
    template_name = "cart.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def test_func(self):
        return True


class CartDetailView(ListView):
    model = CartItem
    template_name = "cart_detail.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()  # Sort by creation time in descending order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here
        return context


class OrderPageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    context_object_name = "products"
    queryset = Product.objects.all()
    template_name = "order_history.html"
    success_url = reverse_lazy("order_history")
    login_url = "login"

    def test_func(self):
        return True


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        # Add product to cart
        return add_to_cart(request, product_id)
    return render(request, "products_detail.html", {"product": product})


def search_results(request):
    query = request.GET.get("keyword", "")
    if query:
        # Perform search in Product model
        search_results = Product.objects.filter(name__icontains=query)
    else:
        search_results = None
    return render(
        request,
        "search_results.html",
        {"search_results": search_results, "keyword": query},
    )
