from django import forms


class ProjectBriefForm(forms.Form):
    WORK_AREA_CHOICES = (
        ('mvp_product', 'MVP & Product Development'),
        ('web_application', 'Custom Web Applications'),
        ('ux_ui', 'UX/UI Design & Prototyping'),
        ('automation', 'AI & Workflow Automation'),
        ('maintenance', 'Maintenance & Technical Support'),
        ('not_sure', 'Not sure yet'),
    )
    PROJECT_STAGE_CHOICES = (
        ('exploring', 'Exploring an idea'),
        ('validating', 'Validating a direction'),
        ('building', 'Building now'),
        ('improving', 'Improving an existing product'),
    )
    TIMING_CHOICES = (
        ('', 'No timeline selected'),
        ('soon', 'Ready to start soon'),
        ('one_to_three_months', 'Within 1–3 months'),
        ('future', 'Exploring a future project'),
        ('not_sure', 'I’m not sure yet'),
    )

    work_area = forms.ChoiceField(choices=WORK_AREA_CHOICES)
    project_stage = forms.ChoiceField(choices=PROJECT_STAGE_CHOICES)
    goal = forms.CharField(min_length=20, max_length=2000)
    name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=320)
    company = forms.CharField(max_length=160, required=False)
    timing = forms.ChoiceField(choices=TIMING_CHOICES, required=False)
    additional_context = forms.CharField(max_length=3000, required=False)
    consent = forms.BooleanField(required=True)
    website = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.HiddenInput,
    )

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_website(self):
        website = self.cleaned_data['website'].strip()
        if website:
            raise forms.ValidationError(
                'Unable to submit this project brief.'
            )
        return website
