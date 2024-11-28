from yaml import serialize
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade
    
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)
    
    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "itens", "total")      


class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True) # Aqui mudou

    class Meta:
        model = Compra
        fields = ("usuario", "itens")


    def create(self, validated_data):
        print("validated_data", validated_data)
        itens_data = validated_data.pop("itens")
        print("itens_data", itens_data)

        compra = Compra.objects.create(**validated_data)
        for item_data in itens_data:
            print("item_data", item_data)
            ItensCompra.objects.create(compra=compra, **item_data)
        compra.save()
        return compra
    

    def update(self, compra, validated_data):
        itens_data = validated_data.pop("itens")
        if itens_data:
            compra.itens.all().delete()
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
        return super().update(compra, validated_data)