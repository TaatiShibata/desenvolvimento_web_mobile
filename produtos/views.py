from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Avaliacao, Produto
from .forms import AvaliacaoForm, EditProfileForm, ProdutoForm, LoginForm, UserRegistrationForm
from django.contrib import messages

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    avaliacoes = Avaliacao.objects.filter(produto=produto)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.produto = produto
            avaliacao.usuario = request.user
            avaliacao.save()
            # Adicione uma mensagem de sucesso aqui, se necessário
            return redirect('produto_detalhe', produto_id=produto_id)
    else:
        form = AvaliacaoForm()

    return render(request, 'produto_detalhe.html', {'produto': produto, 'form': form, 'avaliacoes': avaliacoes})

@login_required
def home(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'index.html', context)

def add_review(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.produto = produto
            avaliacao.usuario = request.user
            avaliacao.save()
            return redirect('product_detail', pk=produto.id)
    else:
        form = AvaliacaoForm()
    return render(request, 'review.html', {'form': form, 'produto': produto})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid form submission.")
            messages.error(request, form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = "Usuário ou senha incorretos. Por favor, tente novamente."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    avaliacoes = Avaliacao.objects.filter(usuario=user)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'profile.html', {
        'user': user,
        'form': form,
        'avaliacoes': avaliacoes
    })

def edit_profile_view(request):
    # Lógica para editar o perfil aqui
    return render(request, 'edit_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def apagar_avaliacao(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)

    # Verifica se o usuário tem permissão para apagar a avaliação
    if avaliacao.usuario == request.user:
        avaliacao.delete()
        messages.success(request, 'Avaliação apagada com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para apagar esta avaliação.')

    return redirect('produto_detalhe', produto_id=avaliacao.produto.id)

@login_required
def registrar_avaliacao(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.produto = produto
            avaliacao.usuario = request.user
            avaliacao.save()
            return redirect('index')
    else:
        form = AvaliacaoForm()

    context = {
        'form': form,
        'produto': produto,
    }
    return render(request, 'registrar_avaliacao.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'product': product})

@login_required
def registrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProdutoForm()
    
    return render(request, 'registrar_produto.html', {'form': form})

def lista_produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'produtos/lista_produtos.html', context)
