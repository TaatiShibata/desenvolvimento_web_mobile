# tests/test_redimensionamento_imagem.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from produtos.models import redimensionar_imagem, MeuModelo
from PIL import Image
import io

class RedimensionamentoImagemTestCase(TestCase):
    def setUp(self):
        # Cria uma imagem temporária para os testes
        buffer = io.BytesIO()
        image = Image.new('RGB', (500, 500))
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        self.imagem = SimpleUploadedFile('test_image.jpg', buffer.read(), content_type='image/jpeg')

    def test_redimensionar_imagem(self):
        largura_maxima = 300
        altura_maxima = 300
        imagem_redimensionada = redimensionar_imagem(self.imagem, largura_maxima, altura_maxima)
        
        # Verifica se a imagem foi redimensionada corretamente
        img = Image.open(imagem_redimensionada)
        self.assertEqual(img.width, largura_maxima)
        self.assertEqual(img.height, altura_maxima)

class MeuModeloTestCase(TestCase):
    def setUp(self):
        # Cria uma instância do modelo com uma imagem para os testes
        self.imagem = SimpleUploadedFile('test_image.jpg', b'')
        self.modelo = MeuModelo.objects.create(imagem=self.imagem)

    def test_resize_image_method(self):
        largura = 200
        altura = 200
        # Chama a função redimensionar_imagem diretamente para testá-la
        imagem_redimensionada = redimensionar_imagem(self.imagem, largura, altura)
        
        # Verifica se a imagem foi redimensionada corretamente
        img = Image.open(imagem_redimensionada)
        self.assertEqual(img.width, largura)
        self.assertEqual(img.height, altura)
