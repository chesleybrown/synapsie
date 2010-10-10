import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from apps.accounts.models import RegistrationManager, RegistrationProfile

# Get an instance of a logger
logger = logging.getLogger('django')

class UserCreationForm(forms.ModelForm):
	"""
	A form that creates a user, with no privileges, from the given username and password.
	"""
	email = forms.EmailField(label=_("Email"),
		help_text = _("A valid email is required."),
		error_messages = {
			'required': _("You must provide an email address."),
			'invalid': _("You must provide a valid email address."),
		})
	username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
		help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
		error_messages = {
			'required': _("You must provide a username."),
			'invalid': _("Your username must contain only letters, numbers and underscores."),
		})
	first_name = forms.RegexField(label=_("First Name"), max_length=30, regex=r'^\w+$',
		error_messages = {
			'required': _("You must provide a first name."),
			'invalid': _("Your first name must contain only letters and be less than 30 characters."),
		})
	last_name = forms.RegexField(label=_("Last Name"), max_length=30, regex=r'^\w+$',
		error_messages = {
			'required': _("You must provide a last name."),
			'invalid': _("Your last name must contain only letters and be less than 30 characters."),
		})
	password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput,
		error_messages = {
			'required': _("You must provide a password."),
			'invalid': _("You must provide a valid password."),
		})
	password2 = forms.CharField(label=_("Confirm"), widget=forms.PasswordInput,
		help_text = _("Enter the same password as above, for verification."),
		error_messages = {
			'required': _("You must verify your password."),
			'invalid': _("Your passwords did not match."),
		})
	
	class Meta:
		model = User
		fields = ("email","username", "first_name", "last_name")
	
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError(_("A user with that email already exists."))
	
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(_("A user with that username already exists."))
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1", "")
		password2 = self.cleaned_data["password2"]
		if password1 != password2:
			raise forms.ValidationError(_("The two password fields didn't match."))
		return password2
	
	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.is_active = False
		if commit:
			user.save()
		return user
	
class UserPasswordResetForm(forms.ModelForm):
	email = forms.EmailField(label=_("Email Address..."),
		help_text = _("A valid email is required."),
		error_messages = {
			'required': _("You must provide an email address."),
			'invalid': _("You must provide a valid email address."),
		})
	
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			raise forms.ValidationError(_("This email does not belong to any account."))
		return email
	
	class Meta:
		model = User
		exclude = ('created', 'username', 'first_name', 'last_name', 'password', 'last_login', 'date_joined')
	
class UserPasswordResetConfirmationForm(forms.ModelForm):
	reset_key = forms.CharField(label=_("Password Reset Key"), widget=forms.HiddenInput(attrs={'readonly':'readonly'}),
		error_messages = {
			'required': _("You must provide a password reset key."),
			'invalid': _("You must provide a valid password reset key."),
		})
	password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput,
		error_messages = {
			'required': _("You must provide a password."),
			'invalid': _("You must provide a valid password."),
		})
	password2 = forms.CharField(label=_("Confirm"), widget=forms.PasswordInput,
		help_text = _("Enter the same password as above, for verification."),
		error_messages = {
			'required': _("You must verify your password."),
			'invalid': _("Your passwords did not match."),
		})
	
	def clean_reset_key(self):
		reset_key = self.cleaned_data["reset_key"]
		user_registration_profile = None
		
		try:
			user_registration_profile = RegistrationProfile.objects.get(reset_key=reset_key)
			
			if user_registration_profile.reset_key_expired():
				raise forms.ValidationError(_("The provided password reset key has expired."))
			
		except RegistrationProfile.DoesNotExist:
			raise forms.ValidationError(_("The provided password reset key is invalid."))
		return reset_key
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1", "")
		password2 = self.cleaned_data["password2"]
		if password1 != password2:
			raise forms.ValidationError(_("The two password fields didn't match."))
		return password2
	
	class Meta:
		model = User
		exclude = ('created', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'password')
	
	def save(self):
		
		# init
		user = None
		user_registration_profile = RegistrationProfile.objects.disable_reset_key(self.cleaned_data['reset_key'])
		
		# key was found and was also disabled, update password
		if user_registration_profile:
			user = user_registration_profile.user
			user.set_password(self.cleaned_data["password1"])
		
		# save changes
		if user:
			user.save()
		return user