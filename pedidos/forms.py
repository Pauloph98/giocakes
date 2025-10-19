from django import forms
from django.utils import timezone

class PedidoForms(forms.Form):
    nome = forms.CharField(
        max_length=60,
        required=True,
        label="Nome",
        widget=forms.TextInput(attrs={"class": "form__nome", "placeholder": "Exemplo: Breno Morim"})
    )
    telefone = forms.CharField(
        max_length=20,
        required=True,
        label="Número de Telefone",
        widget=forms.TextInput(attrs={"class": "form__telefone", "placeholder": "Exemplo: 11 91234-5678"})
    )
    nome_retirada = forms.CharField(
        max_length=60,
        required=True,
        label="Nome de quem irá retirar",
        widget=forms.TextInput(attrs={"class": "form__nome-retirada", "placeholder": "Exemplo: Ana Silva"})
    )
    data_retirada = forms.DateField(
        input_formats=["%d/%m/%Y"],
        required=True,
        label="Data para retirada",
        widget=forms.DateInput(attrs={"class": "form__data-retirada", "placeholder": "Exemplo: 20/02/2023"}, format="%d/%m/%Y"),
        initial=timezone.now  # Definindo o valor inicial como a data atual
    )
    mensagem = forms.CharField(
        required=False,
        max_length=255,
        label="Mensagem (Opcional)",
        widget=forms.Textarea(attrs={"class": "form__mensagem", "placeholder": "Observações sobre o pedido"})
    )

    def clean_data_retirada(self):
        data_retirada = self.cleaned_data.get("data_retirada")
        data_minima = timezone.now().date()

        if data_retirada < data_minima:
            raise forms.ValidationError("A data de retirada não pode ser anterior à data atual.")

        return data_retirada
