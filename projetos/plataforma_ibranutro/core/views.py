from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Document, Profile
from .utils import youtube_embed
from .forms import DocumentForm, ProfileForm, UserForm


@login_required
def dashboard(request):
    courses = (
        Course.objects.filter(is_active=True)
        .prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.order_by("order_index", "id"))
        )
        .order_by("id")
    )

    current_lesson = None
    first_course = courses.first()
    if first_course:
        current_lesson = first_course.lessons.first()

    if current_lesson:
        current_lesson.embed_url = youtube_embed(current_lesson.youtube_url)

    return render(request, "core/dashboard.html", {
        "courses": courses,
        "current_lesson": current_lesson,
    })


@login_required
def lesson_detail(request, lesson_id: int):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    courses = (
        Course.objects.filter(is_active=True)
        .prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.order_by("order_index", "id"))
        )
        .order_by("id")
    )

    lesson.embed_url = youtube_embed(lesson.youtube_url)

    return render(request, "core/dashboard.html", {
        "courses": courses,
        "current_lesson": lesson,
    })


@login_required
def profile_view(request):
    # garante que o profile existe
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")
        else:
            messages.error(request, "Revise os campos do perfil.")
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=profile)

    return render(request, "core/profile.html", {
        "profile": profile,
        "uform": uform,
        "pform": pform,
    })


@login_required
def docs_view(request):
    docs = Document.objects.all().order_by("-id")
    form = DocumentForm()
    return render(request, "core/docs.html", {"docs": docs, "form": form})


@login_required
def doc_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Documento adicionado!")
        else:
            messages.error(request, "Não foi possível adicionar. Revise os campos.")
    return redirect("docs")


@login_required
def doc_edit(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, "Documento atualizado!")
            return redirect("docs")
        else:
            messages.error(request, "Não foi possível salvar. Revise os campos.")
    else:
        form = DocumentForm(instance=doc)

    return render(request, "core/doc_edit.html", {"form": form, "doc": doc})


@login_required
def doc_delete(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    if request.method == "POST":
        doc.delete()
        messages.success(request, "Documento removido!")
    return redirect("docs")
