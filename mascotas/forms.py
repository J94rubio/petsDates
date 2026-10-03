from django import forms

from .models import Mascota


class MascotaForm(forms.ModelForm):

    class Meta:
        model = Mascota

        fields = [
            'nombre',
            'especie',
            'raza',
            'edad',
            'propietario',
        ]

        widgets = {

            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Milú',
                }
            ),

            'especie': forms.Select(
                choices=[
                    ('', 'Seleccione una especie'),
                    ('Perro', 'Perro'),
                    ('Gato', 'Gato'),
                    ('Ave', 'Ave'),
                    ('Conejo', 'Conejo'),
                    ('Hamster', 'Hámster'),
                    ('Tortuga', 'Tortuga'),
                    ('Pez', 'Pez'),
                    ('Otro', 'Otro'),
                ],
                attrs={
                    'class': 'form-control',
                }
            ),

            'raza': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Labrador',
                }
            ),

            'edad': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'placeholder': 'Edad en años',
                }
            ),

            'propietario': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del propietario',
                }
            ),
        }

    def clean_nombre(self):

        nombre = self.cleaned_data['nombre']

        if len(nombre.strip()) < 2:
            raise forms.ValidationError(
                'El nombre debe tener al menos 2 caracteres.'
            )

        return nombre

    def clean_edad(self):

        edad = self.cleaned_data['edad']

        if edad < 0:
            raise forms.ValidationError(
                'La edad no puede ser negativa.'
            )

        return edad