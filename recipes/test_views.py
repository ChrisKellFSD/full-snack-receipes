from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Comment


class TestViews(TestCase):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_all_recipes_page(self):
        response = self.client.get('/all_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_recipes.html')

    def test_get_my_recipes_page(self):
        response = self.client.get('/my_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_recipes.html')

    # def test_get_add_recipes_page(self):
    #     self.client.login()
    #     response = self.client.get('/add_recipe/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'recipe_form.html')

    # def test_get_recipe_detail_page(self):
    #     recipe = Recipe.objects.create(title='Test Recipe', excerpt='test', ingredients='test', method='test')
    #     response = self.client.get(f'/recipe_detail/{recipe.slug}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'recipe_detail.html')

    # def test_get_update_recipe_page(self):
    #     recipe = Recipe.objects.create(title='Test Recipe', excerpt='test', ingredients='test', method='test')
    #     response = self.client.get(f'/update_recipe/{self.recipe.slug}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'update_recipe.html')

    def test_get_searched_recipes_page(self):
        response = self.client.get('/search_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_recipes.html')

    def test_get_your_recipes_page_if_user_logged_out(self):
        self.client.logout()
        response = self.client.get('/my_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_recipes.html')

    def test_can_add_recipe(self):
        self.client.post('/add_recipe/', {
            'title': 'Test Title',
            'excerpt': 'Test Excerpt',
            'ingredients': 'Test Ingredients',
            'method': 'Test Method'
        })
        new_recipe = Recipe.objects.filter(title='Test Title')
        self.assertEqual(len(new_recipe), 0)

    # def test_can_edit_recipe(self):
    #     self.client.post(f'/update_recipe/{self.recipe.slug}', {
    #         'title': 'Edited Title',
    #         'excerpt': 'Test Excerpt',
    #         'ingredients': 'Test Ingredients',
    #         'method': 'Test Method'
    #     })
    #     edited_recipe = Recipe.objects.first().title
    #     self.assertEqual(edited_recipe, "Edited Title")

    # def test_can_delete_recipe(self):
    #     author = User.objects.create(username='example_username')
    #     recipe = Recipe.objects.create(
    #         title='Example Recipe',
    #         slug='example-recipe',
    #         author=author,
    #         excerpt='This is an example recipe.',
    #         ingredients='This is an example ingredient.',
    #         method='This is an example method.'
    #         )
    #     response = self.client.get(f'/delete_recipe/{recipe.slug}')
    #     self.assertRedirects(response, '/my_recipes/')

    def test_number_of_likes(self):

        author = User.objects.create(username='example_username')
        recipe = Recipe.objects.create(
            title='Example Recipe',
            slug='example-recipe',
            author=author,
            excerpt='This is an example recipe.',
            ingredients='This is an example ingredient.',
            method='This is an example method.'
            )
    
    # Create a few User instances to use as 'likes' for the Recipe
        user_1 = User.objects.create(username='user_1')
        user_2 = User.objects.create(username='user_2')
        user_3 = User.objects.create(username='user_3')
    
    # Add the 'likes' to the Recipe instance
        recipe.likes.add(user_1, user_2, user_3)
    
    # Assert that the number_of_likes() method returns the correct number of likes
        self.assertEqual(recipe.number_of_likes(), 3)


