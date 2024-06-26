from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# No arquivo models.py da sua aplicação

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos', null=True, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagem:
            img = Image.open(self.imagem.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.imagem.path)
    
class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.produto} por {self.usuario}"

def redimensionar_imagem(imagem, largura_maxima, altura_maxima):
    img = Image.open(imagem)
    largura, altura = img.size

    # Calcula as proporções para redimensionamento
    proporcao = min(largura_maxima / largura, altura_maxima / altura)

    # Redimensiona a imagem mantendo a proporção
    nova_largura = int(largura * proporcao)
    nova_altura = int(altura * proporcao)
    img = img.resize((nova_largura, nova_altura), Image.ANTIALIAS)

    # Converte a imagem de volta para o formato de arquivo Django
    img_io = BytesIO()
    img.save(img_io, format='JPEG' if imagem.name.endswith('.jpg') else 'PNG', quality=100)
    img_file = InMemoryUploadedFile(
        img_io, None, imagem.name, 'image/jpeg' if imagem.name.endswith('.jpg') else 'image/png', sys.getsizeof(img_io), None
    )
    return img_file

class MeuModelo(models.Model):
    imagem = models.ImageField(upload_to='diretorio_de_upload/')

def resize_image(image, width, height):
    img = Image.open(image)
    img.thumbnail((width, height), Image.ANTIALIAS)
    img.save(image.path)