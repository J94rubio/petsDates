from django import forms


class CitaForm(forms.Form):

    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d'
        ),
        input_formats=[
            '%Y-%m-%d'
        ]
    )

    motivo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Vacunación anual',
            }
        )
    )

    estado = forms.ChoiceField(
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Confirmada', 'Confirmada'),
            ('Completada', 'Completada'),
            ('Cancelada', 'Cancelada'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    
# from django import forms

# from .models import Cita


# class CitaForm(forms.ModelForm):

#     class Meta:
#         model = Cita

#         fields = [
#             'fecha',
#             'motivo',
#             'estado',
#         ]

#         widgets = {

#             'fecha': forms.DateInput(
#                 attrs={
#                     'type': 'date',
#                     'class': 'form-control',
#                 },
#                 format='%Y-%m-%d'
#             ),

#             'motivo': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Ej: Vacunación anual',
#                 }
#             ),

#             'estado': forms.Select(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#         }

#     def __init__(self, *args, **kwargs):

#         super().__init__(*args, **kwargs)

#         self.fields['fecha'].input_formats = [
#             '%Y-%m-%d'
#         ]