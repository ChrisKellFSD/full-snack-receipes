from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Recipe
from .forms import CommentForm, RecipeForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.post_id = recipe.id
            comment.save()
            messages.success(request, "Thank you. Your comment was submitted successfully!")
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class RecipeLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Recipe, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class AddRecipe(SuccessMessageMixin, CreateView):
    model = Recipe
    template_name = 'recipe_form.html'
    form_class = RecipeForm
    success_message = 'Recipe Successfully Added'
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdateRecipe(SuccessMessageMixin, UpdateView):
    model = Recipe
    template_name = 'update_recipe.html'
    form_class = RecipeForm
    success_message = 'Recipe Successfully Updated'
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
        

def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe.delete()
    messages.success(request, 'Recipe Deleted Successfully')
    return redirect(reverse('my_recipes'))


def search_recipes(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        recipes = Recipe.objects.filter(title__icontains=searched)
        return render(request, 'search_recipes.html', {
            'searched': searched, 'recipes': recipes
            })
    else:
        return render(request, 'search_recipes.html')


class UsersRecipeList(View):
    def get(self, request):
        if request.user.is_authenticated:
            recipes = Recipe.objects.filter(author=request.user)
            paginator = Paginator(recipes, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'my_recipes.html', {'page_obj': page_obj})
        else:
            return render(request, 'my_recipes.html')