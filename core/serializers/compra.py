from rest_framework.serializers import ModelSerializer, CharField

from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = "__all__"

class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = "__all__"