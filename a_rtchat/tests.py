from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from a_users.models import Profile

class SignUpTest(TestCase):
    def test_sign_up_page_exists(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        
    def test_sign_up_user(self):
        user_data = {
            'email' : 'test@email.com',
            'username' : 'testuser',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        response = self.client.post(reverse('account_signup'), user_data, format='text/html')
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('profile', args=[user_data['username']]))
        self.assertEqual(response.status_code, 200)
        
        
class BaseSetUp(TestCase): 
    
    def setUp(self):
        user_data = {
            'email' : 'test2@email.com',
            'username' : 'testuser',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        self.client.post(reverse('account_signup'), user_data, format='text/html')
        

class ProfileEditTest(BaseSetUp): 
    
    def test_profile_edit(self):
        response = self.client.get(reverse('profile-edit')) 
        self.assertEqual(response.status_code, 200) 
        
        form_data = {
            'email' : 'test2@email.com'
        }
        response = self.client.post(reverse('profile-edit'), data=form_data)
        self.assertEqual(response.status_code, 302) 
        
        self.user = User.objects.get(username='testuser')
        self.assertEqual(self.user.email, 'test2@email.com')
        
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.email, 'test2@email.com')
        
