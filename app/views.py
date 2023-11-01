from django.shortcuts import get_object_or_404  # views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import UserForm, LoginForm, CompetitionForm, TriviaQuestionForm, CompetitionSettingsForm
from .models import Competition, CompetitionTrivia, Trivia, User
from .utils import generate_random_string
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import F
from .trivia_cache import TriviaCache
@login_required
def home(request):
    return render(request, "home.html")


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def login_or_register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form_type = request.POST.get("type")
        if form_type == "signup":
            form = UserForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                user = User.objects.create(username=username)
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, "Account = Created!")

                next_url = request.POST.get("next", None)

                # if there is a next parameter, redirect the user to that URL
                if next_url:
                    return redirect(next_url, permanent=True)

                return redirect("home", permanent=True)
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif form_type == "login":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, "You're all logged in!")

                    return redirect("home")
                else:
                    messages.error(request, "Invalid login credentials.")

            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UserForm()

    return render(request, "login.html", {"form": form})


@login_required
def comp_create(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.owner = request.user  # Assign the current user as the owner
            competition.code = generate_random_string(16)
            competition.save()
            return redirect("comp_setup", competition.code)
        else:
            # Form has errors, flash error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return redirect("home")


@login_required
def comp_join(request):
    if request.method == "POST":
        # Handle the form submission to join a competition
        # You can access form data using request.POST
        competition_id = request.POST.get("name")
        # Perform actions to join the competition with the provided competition_id
        # Example: Add the user as a participant in the competition
        # participant = Participant.objects.create(competition_id=competition_id, user=request.user)
        return redirect("home")  # Redirect to the competition detail page

    return render(request, "comp_join.html")


@login_required
def comp_setup(request, comp_code):
    comp = get_object_or_404(Competition, code=comp_code)
    if request.method == "POST":
        trivia_form = TriviaQuestionForm(request.POST)
        settings_form = CompetitionSettingsForm(request.POST)

        if trivia_form.is_valid():
            num_questions = trivia_form.cleaned_data["num_questions"]
            category = trivia_form.cleaned_data["category"]
            question_type = trivia_form.cleaned_data["question_type"]
            difficulty = trivia_form.cleaned_data["difficulty"]
            cache = TriviaCache()
            questions = cache.get_trivia(num_questions, category, difficulty, question_type, comp)
            # api = OpenTriviaAPI()
            # question_data = api.fetch_questions(
            #     num_questions,
            #     category,
            #     difficulty,
            #     question_type,
            # )
            # questions = save_trivia_data_from_api(question_data, comp)
            return JsonResponse({"questions": questions})

        elif settings_form.is_valid():
            if settings_form.cleaned_data["start_competition"]:
                comp.started = True

            end_time = settings_form.cleaned_data["end_time"]
            if end_time:
                comp.end_time = end_time
            comp.save()
            return redirect("comp_setup", comp_code)

    questions = comp.trivia_set.annotate(category_name=F("category__name")).values()
    return render(
        request,
        "comp_setup.html",
        {
            "trivia_form": TriviaQuestionForm(),
            "settings_form": CompetitionSettingsForm(initial={"start_competition": comp.started}),
            "questions": questions,
            "competition": comp,
        },
    )

@login_required
@require_POST
def delete_question(request, comp_code):
    comp = get_object_or_404(Competition, code=comp_code, owner=request.user)
    # Get the question ID to be deleted from the request
    question_id = request.POST.get("question_id")
    question = get_object_or_404(Trivia, id=question_id)
    # Ensure that the question exists in the competition
    try:
        competition_trivia = CompetitionTrivia.objects.get(competition=comp, trivia=question)
        competition_trivia.delete()
    except CompetitionTrivia.DoesNotExist:
        return JsonResponse({"error": "Question not found or not authorized to delete."}, status=400)
    
    return JsonResponse({"message": "Question deleted successfully"})