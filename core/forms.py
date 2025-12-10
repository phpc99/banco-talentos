from django import forms
from .models import Candidato

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = [
            'nome',
            'estado',
            'cidade',
            'formacao',
            'area',
            'curriculo',
            'foto',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():          # deixa tudo obrigatório...
            field.required = True
        self.fields['curriculo'].required = False   # ...menos curriculo e
        self.fields['foto'].required = False        # foto