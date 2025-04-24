from django import forms
from django.forms import modelformset_factory

from dispatchers.models import Handover


class HandoverForm(forms.ModelForm):
    class Meta:
        model = Handover
        exclude = ['handover_id']

    shift_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control handover-form-control',
            'type': 'date',
            'id': 'todayDate',
        })
    )

    SHIFT_CHOICES = [
        ('', 'Select Shift'),
        ('DS', 'DS'),
        ('NS', 'NS'),
        ('SS', 'SS'),
    ]

    shift = forms.ChoiceField(
        choices=SHIFT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control handover-form-control',
            'id': 'shift',
            'required': True
        })
    )

    dispatcher_name = forms.CharField(
        initial="",
        widget=forms.TextInput(attrs={
            'class': 'form-control handover-form-control',
            'id': 'dispatcher',
            'readonly': True,
        })
    )

    chief_duty_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control handover-form-control',
            'id': 'chief_duty_dispatcher',
        })
    )

    shift_highlights = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'id': 'shift_highlights',
            'rows': 2,
        })
    )

    non_standard_flights = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    naifr = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    aog = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    comat_flights = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    fob_created_aog = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input handover-form-check-input',
            'id': 'fob_created_aog',

        })
    )

    remarks_created_com = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input handover-form-check-input',
            'id': 'remarks_added',
        })
    )

    weather_issues = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'id': 'weather_issues',
            'rows': 2,
        })
    )

    fuel_payload_critical = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
        })
    )

    operational_notams = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
            'id': 'notams'
        })
    )

    enroute_weather = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
        })
    )

    mels = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
            'id': 'mels',
        })
    )

    cdd_network_summary = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
        })
    )

    misc = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
        })
    )

    it_issues = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
        })
    )

    navblue_tickets = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
            'id': 'navblue_tickets',
        })
    )

    procedural_changes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control handover-form-control',
            'rows': 2,
            'id': 'procedural_changes',
        })
    )



