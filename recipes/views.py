from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Recipe
from .forms import CommentForm, RecipeForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4


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
    fields = ['title', 'ingredients', 'method', 'featured_image']