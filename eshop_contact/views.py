# Import necessary modules and functions from Django
from django.shortcuts import render
from .forms import CreateContactForm
from .models import ContactUs
from eshop_settings.models import SiteSetting


# Define the view function for the contact page
def contact_page(request):
    # Create an instance of the contact form, populated with POST data if available
    contact_form = CreateContactForm(request.POST or None)

    # Check if the form is valid (i.e., all required fields are filled and data is correct)
    if contact_form.is_valid():
        # Extract cleaned data from the form
        full_name = contact_form.cleaned_data.get("full_name")
        email = contact_form.cleaned_data.get("email")
        subject = contact_form.cleaned_data.get("subject")
        text = contact_form.cleaned_data.get("text")

        # Create a new ContactUs object with the form data and set is_read to False
        ContactUs.objects.create(full_name=full_name, email=email, subject=subject, text=text, is_read=False)

        # Reset the contact form for the next submission
        contact_form = CreateContactForm()

    # Retrieve the site settings
    setting = SiteSetting.objects.first()

    # Prepare the context dictionary to pass to the template
    context = {"contact_form": contact_form, "setting": setting}

    # Render the contact page template with the contact form and site settings context
    return render(request, 'contact_us/contact_us_page.html', context)
