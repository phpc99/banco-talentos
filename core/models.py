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

    nome = models.CharField(max_length=150)
    estado = models.CharField(max_length=2, choices=ESTADOS)
    cidade = models.CharField(max_length=100)
    formacao = models.CharField(max_length=10, choices=FORMACOES)
    area = models.CharField(max_length=10, choices=AREAS)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    anotacoes = models.TextField(blank=True, null=True) # campo exclusivo do gestor, pode deixar em branco
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome