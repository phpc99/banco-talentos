from django.db import models

# Create your models here.

class Candidato(models.Model):
    ESTADOS = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    FORMACOES = [
        ('LIC', 'Licenciatura'),
        ('MES', 'Mestrado'),
        ('DOUT', 'Doutorado'),
    ]

    AREAS = [
        ('CONT_I', 'Contador I'),
        ('CONT_II', 'Contador II'),
        ('CONT_III', 'Contador III'),
        ('AUD_I', 'Auditor I'),
        ('AUD_II', 'Auditor II'),
        ('AUD_III', 'Auditor III'),
    ]

    STATUS_SUBMETIDO = 'SUBMETIDO'
    STATUS_ENTREVISTA = 'ENTREVISTA'
    STATUS_APROVADO = 'APROVADO'
    STATUS_REPROVADO = 'REPROVADO'
    STATUS_NAO_COMPARECEU = 'NAO_COMPARECEU'

    STATUS_CHOICES = [
        (STATUS_SUBMETIDO, 'Cadastro submetido'),
        (STATUS_ENTREVISTA, 'Selecionado para entrevista'),
        (STATUS_APROVADO, 'Resultado final: aprovado'),
        (STATUS_REPROVADO, 'Resultado final: reprovado'),
        (STATUS_NAO_COMPARECEU, 'Resultado final: não compareceu'),
    ]

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True) # um email por cadastro / fica como camada extra
    estado = models.CharField(max_length=2, choices=ESTADOS)
    cidade = models.CharField(max_length=100)
    formacao = models.CharField(max_length=10, choices=FORMACOES)
    area = models.CharField(max_length=10, choices=AREAS)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    anotacoes = models.TextField(blank=True, null=True) # campo exclusivo do gestor, pode deixar em branco
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMETIDO # todo cadastro já nasce submetido GG
    )

    def __str__(self):
        return self.nome
    


class EntrevistaAvaliacao(models.Model):
    DECIDIR_DEPOIS = "DECIDIR_DEPOIS"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    NAO_COMPARECEU = "NAO_COMPARECEU"

    DECISAO_CHOICES = [
        (DECIDIR_DEPOIS, "Decidir depois"),
        (APROVADO, "Aprovado"),
        (REPROVADO, "Reprovado"),
        (NAO_COMPARECEU, "Não compareceu"),
    ]

    candidato = models.OneToOneField(
        "Candidato",
        on_delete=models.CASCADE,
        related_name="entrevista"
    )

    # Guarda perguntas/respostas/notas em JSON:
    # {
    #   "comum": [{"pergunta": "...", "nota": "RUIM|MEDIO|DESEJAVEL|MUITO_BOM", "observacao": "..."}],
    #   "especifico": [...]
    # }
    respostas = models.JSONField(default=dict, blank=True)

    decisao = models.CharField(
        max_length=20,
        choices=DECISAO_CHOICES,
        default=DECIDIR_DEPOIS
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    entrevistado = models.BooleanField(default=False)

    def __str__(self):
        return f"Entrevista - {self.candidato.nome}"
