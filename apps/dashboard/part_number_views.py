from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from apps.task.models import PartNumber
from django.db.models import Q

class PartNumberListView(LoginRequiredMixin, ListView):
    model = PartNumber
    template_name = 'master_data/part_number/part_number_list.html'
    context_object_name = 'part_numbers'
    ordering = ['-created_at']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(part_number__icontains=search_query) |
                Q(item__icontains=search_query)
            )
        return queryset

class PartNumberCreateView(LoginRequiredMixin, CreateView):
    model = PartNumber
    template_name = 'master_data/part_number/part_number_form.html'
    fields = ['part_number', 'item']
    success_url = reverse_lazy('dashboard-part-number-list')

    def form_valid(self, form):
        messages.success(self.request, 'Part Number created successfully.')
        return super().form_valid(form)

class PartNumberUpdateView(LoginRequiredMixin, UpdateView):
    model = PartNumber
    template_name = 'master_data/part_number/part_number_form.html'
    fields = ['part_number', 'item']
    success_url = reverse_lazy('dashboard-part-number-list')

    def form_valid(self, form):
        messages.success(self.request, 'Part Number updated successfully.')
        return super().form_valid(form)

class PartNumberDeleteView(LoginRequiredMixin, DeleteView):
    model = PartNumber
    template_name = 'master_data/part_number/part_number_confirm_delete.html'
    success_url = reverse_lazy('dashboard-part-number-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Part Number deleted successfully.')
        return super().delete(request, *args, **kwargs)
