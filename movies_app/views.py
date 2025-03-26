from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Movie
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Função para exibir os filmes
def index(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies, 'query': query})

def report(request):
    # Obtém todos os filmes da base de dados
    movies = Movie.objects.all()
    # Passa os filmes para o template
    return render(request, 'report.html', {'movies': movies})

def watch_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.watched = True
    movie.save()
    return redirect('index')

# Função para adicionar um filme
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        if title and genre:
            Movie.objects.create(title=title, genre=genre)
    return redirect('index')

# Função para editar um filme
def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.genre = request.POST.get('genre')
        movie.save()
        return redirect('index')
    return render(request, 'edit_movie.html', {'movie': movie})

# Função para excluir um filme
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return redirect('index')

# Função para exportar filmes (XLS ou PDF)
def export_movies(request):
    format_type = request.GET.get('format', 'xls')
    if format_type == 'xls':
        return export_to_xls(request)
    elif format_type == 'pdf':
        return export_to_pdf(request)
    return HttpResponse("Invalid export format", status=400)

# Função para exportar para XLS
def export_xls(request):
    # Criação da resposta em XLS
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="filmes.xlsx"'

    # Criando um arquivo Excel com openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Filmes"

    # Escrevendo os cabeçalhos
    ws.append(['Título', 'Gênero', 'Status'])

    # Adicionando os filmes no arquivo XLS
    movies = Movie.objects.all()
    for movie in movies:
        ws.append([movie.title, movie.genre, 'Assistido' if movie.watched else 'Não Assistido'])

    wb.save(response)
    return response

def export_pdf(request):
    # Criação da resposta em PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filmes.pdf"'

    # Criando o objeto PDF com reportlab
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Relatório de Filmes")
    p.drawString(100, 730, "Título | Gênero | Status")

    # Definindo as coordenadas para o início da lista de filmes
    y_position = 710

    # Iterando sobre todos os filmes e adicionando no PDF
    movies = Movie.objects.all()
    for movie in movies:
        p.drawString(100, y_position, f"{movie.title} | {movie.genre} | {'Assistido' if movie.watched else 'Não Assistido'}")
        y_position -= 20  # Decrementando a posição para o próximo filme

    p.showPage()
    p.save()

    return response
