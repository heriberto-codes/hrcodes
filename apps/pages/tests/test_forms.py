from django.test import SimpleTestCase

from apps.pages.forms import ProjectBriefForm


class ProjectBriefFormTests(SimpleTestCase):
    def valid_data(self, **overrides):
        data = {
            'work_area': 'web_application',
            'project_stage': 'building',
            'goal': 'Replace a manual intake workflow with a useful product.',
            'name': 'Ada Lovelace',
            'email': 'ADA@EXAMPLE.COM',
            'company': 'Analytical Engines',
            'timing': 'one_to_three_months',
            'additional_context': 'The current process uses spreadsheets.',
            'consent': True,
            'website': '',
        }
        data.update(overrides)
        return data

    def test_accepts_valid_data_and_normalizes_email(self):
        data = self.valid_data(
            email='  ADA@EXAMPLE.COM  ',
            company='',
            timing='',
            additional_context='',
        )

        form = ProjectBriefForm(data=data)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['email'], 'ada@example.com')
        self.assertEqual(form.cleaned_data['company'], '')
        self.assertEqual(form.cleaned_data['timing'], '')
        self.assertEqual(form.cleaned_data['additional_context'], '')

    def test_rejects_missing_required_fields(self):
        for field_name in (
            'work_area',
            'project_stage',
            'goal',
            'name',
            'email',
            'consent',
        ):
            with self.subTest(field=field_name):
                data = self.valid_data()
                data.pop(field_name)
                form = ProjectBriefForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(field_name, form.errors)

    def test_rejects_invalid_choices_formats_and_length_boundaries(self):
        invalid_values = (
            ('work_area', 'unknown-service'),
            ('project_stage', 'unknown-stage'),
            ('timing', 'unknown-timing'),
            ('goal', 'Too short'),
            ('goal', 'x' * 2001),
            ('name', 'x' * 121),
            ('email', 'not-an-email'),
            ('company', 'x' * 161),
            ('additional_context', 'x' * 3001),
        )

        for field_name, value in invalid_values:
            with self.subTest(field=field_name, value_length=len(value)):
                form = ProjectBriefForm(
                    data=self.valid_data(**{field_name: value})
                )

                self.assertFalse(form.is_valid())
                self.assertIn(field_name, form.errors)

    def test_rejects_populated_honeypot(self):
        form = ProjectBriefForm(
            data=self.valid_data(website='https://spam.example')
        )

        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)
        self.assertIn(
            'Unable to submit this project brief.',
            form.errors['website'],
        )
