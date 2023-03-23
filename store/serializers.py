from rest_framework import serializers
from . models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    subcategory = serializers.IntegerField(source='subcategory_id')

    class Meta:
        model = Product
        # fields = ['name', 'content', 'id', 'subcategory_id', 'image', 'viewed', 'insert_date']
        fields = '__all__'