from django.contrib.auth.mixins import LoginRequiredMixin # for authorized
from django.views import generic
from .models import Article
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

# Create your views here.
class ArticleCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body', )
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleListView(generic.ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user :
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ArticleDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user :
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
