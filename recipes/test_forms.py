from django.test import TestCase
from .forms import RecipeForm, CommentForm


class TestRecipeForm(TestCase):

    def test_recipe_title_is_required(self):
        form = RecipeForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_recipe_excerpt_is_required(self):
        form = RecipeForm({'excerpt': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('excerpt', form.errors.keys())
        self.assertEqual(form.errors['excerpt'][0], 'This field is required.')

    def test_recipe_ingredients_is_required(self):
        form = RecipeForm({'ingredients': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('ingredients', form.errors.keys())
        self.assertEqual(form.errors['ingredients'][0], 'This field is required.')

    def test_recipe_method_is_required(self):
        form = RecipeForm({'method': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('method', form.errors.keys())
        self.assertEqual(form.errors['method'][0], 'This field is required.')

    def test_fields_are_explicit_in_form_metaclass(self):
        form = RecipeForm()
        self.assertEqual(form.Meta.fields, ('title', 'excerpt', 'ingredients', 'method', 'featured_image', 'status'))

    def test_non_required_fields_are_not_required(self):
        form = RecipeForm(
            {
                'featured_image': 'Test', 'status': 'Test'
                }
            )
        self.assertFalse(form.is_valid())


class TestCommentForm(TestCase):

    def test_body_field_is_required(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')