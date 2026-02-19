from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


# --- Category Admin ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_count")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="# Products")
    def product_count(self, obj):
        count = obj.product_set.count()
        color = "#a855f7" if count > 0 else "#6b6890"
        return format_html(
            '<span style="font-weight:700; color:{};">{}</span>', color, count
        )


# --- Product Admin ---

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # -- List view --
    list_display = (
        "image_thumbnail",
        "name",
        "category",
        "price",
        "stock",
        "stock_status",
    )
    list_display_links = ("image_thumbnail", "name")
    list_editable = ("price", "stock")
    list_filter = ("category",)
    search_fields = ("name", "description", "category__name")
    list_per_page = 20
    ordering = ("name",)

    # -- Detail / edit form --
    readonly_fields = ("image_preview",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("name", "description", "category"),
                "classes": ("wide",),
            },
        ),
        (
            "Pricing and Stock",
            {
                "fields": ("price", "stock"),
                "classes": ("wide",),
            },
        ),
        (
            "Product Image",
            {
                "fields": ("image", "image_preview"),
                "classes": ("wide",),
                "description": "Upload a product photo. Recommended: square image, min 600x600px.",
            },
        ),
    )

    # -- Custom display methods --

    @admin.display(description="Image")
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="'
                "width:56px; height:56px; object-fit:cover;"
                'border-radius:8px; border:2px solid #7c3aed;" />',
                obj.image.url,
            )
        return format_html(
            '<div style="'
            "width:56px; height:56px; border-radius:8px;"
            "background:linear-gradient(135deg,#7c3aed,#ec4899);"
            "display:flex; align-items:center; justify-content:center;"
            'font-size:1.4rem; font-weight:800; color:white;">{}</div>',
            obj.name[0].upper() if obj.name else "?",
        )

    @admin.display(description="Stock Status")
    def stock_status(self, obj):
        if obj.stock == 0:
            badge = ("Out of Stock", "#ef4444", "#2d1010")
        elif obj.stock <= 5:
            badge = ("Low Stock", "#f59e0b", "#2d2010")
        else:
            badge = ("In Stock", "#10b981", "#0d2d1e")
        label, color, bg = badge
        return format_html(
            '<span style="'
            "padding:4px 10px; border-radius:20px;"
            "font-size:0.78rem; font-weight:600;"
            "color:{}; background-color:{};"
            'white-space:nowrap;">{}</span>',
            color, bg, label,
        )

    @admin.display(description="Current Image Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="'
                "max-height:280px; max-width:100%; object-fit:contain;"
                'border-radius:12px; border:2px solid #7c3aed;" />',
                obj.image.url,
            )
        return format_html(
            '<p style="color:#6b6890; font-style:italic;">{}</p>',
            "No image uploaded yet.",
        )
