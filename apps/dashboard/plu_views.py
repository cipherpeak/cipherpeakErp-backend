from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from apps.task.models import PLU

class PLUListView(LoginRequiredMixin, ListView):
    model = PLU
    template_name = 'master_data/plu/plu_list.html'
    context_object_name = 'plus'
    ordering = ['-created_at']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(plu__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(sub_service__name__icontains=search_query)
            )
            
        return queryset

class PLUCreateView(LoginRequiredMixin, CreateView):
    model = PLU
    template_name = 'master_data/plu/plu_form.html'
    fields = ['plu', 'category', 'sub_service']
    success_url = reverse_lazy('dashboard-plu-list')

    def form_valid(self, form):
        messages.success(self.request, 'PLU created successfully.')
        return super().form_valid(form)

class PLUUpdateView(LoginRequiredMixin, UpdateView):
    model = PLU
    template_name = 'master_data/plu/plu_form.html'
    fields = ['plu', 'category', 'sub_service']
    success_url = reverse_lazy('dashboard-plu-list')

    def form_valid(self, form):
        messages.success(self.request, 'PLU updated successfully.')
        return super().form_valid(form)

class PLUDeleteView(LoginRequiredMixin, DeleteView):
    model = PLU
    template_name = 'master_data/plu/plu_confirm_delete.html'
    success_url = reverse_lazy('dashboard-plu-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'PLU deleted successfully.')
        return super().delete(request, *args, **kwargs)
