import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect

from core.pos.forms import Pedido, PedidoForm
from core.security.mixins import PermissionMixin


class PedidoListView(PermissionMixin, ListView):
    model = Pedido
    template_name = 'pedido/list.html'
    permission_required = 'view_pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['create_url'] = reverse_lazy('pedido_create')
        context['title'] = 'Listado de Pedidos'
        return context

def update_estado(request,id):
    pedido = Pedido.objects.get(id = id)
    pedido.activo = False
    pedido.save()
    #messages.success(request, "Estado del pedido actualizado")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))