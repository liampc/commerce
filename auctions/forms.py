from django import forms


class Add_listing(forms.Form):
    product = forms.CharField(label="Listing name" ,max_length=64)
    price = forms.DecimalField(label="Starting price", max_digits=12, decimal_places=2)
    description = forms.CharField(label="Description",widget=forms.Textarea, required=False)
    product_image = forms.ImageField(label="Product", required=False,)
    image_url = forms.URLField(label="Image URL", required=False)
    category = forms.CharField(label="Category", max_length=64)


class Add_bid(forms.Form):
    bid_price = forms.DecimalField(max_digits=12, decimal_places=2)