# tests/test_models.py
from django.test import TestCase
from meu_app.models import Produto, Avaliacao
from django.contrib.auth.models import User

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(nome='Produto Teste', descricao='Descrição do produto', preco=100.00)

    def test_produto_creation(self):
        self.assertEqual(self.produto.nome, 'Produto Teste')
        self.assertEqual(self.produto.descricao, 'Descrição do produto')
        self.assertEqual(self.produto.preco, 100.00)

class AvaliacaoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.produto = Produto.objects.create(nome='Produto Teste', descricao='Descrição do produto', preco=100.00)
        self.avaliacao = Avaliacao.objects.create(produto=self.produto, usuario=self.user, nota=4, comentario='Bom produto')

    def test_avaliacao_creation(self):
        self.assertEqual(self.avaliacao.produto, self.produto)
        self.assertEqual(self.avaliacao.usuario, self.user)
        self.assertEqual(self.avaliacao.nota, 4)
        self.assertEqual(self.avaliacao.comentario, 'Bom produto')
