import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .forms import UserForm
from .models import Voting, VoteFact, VoteVariant, User


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'votings', 'name': 'Голосования'}
    ]


def new_update_message(le, header, body):
    return {
        "heading": "heading" + str(le),
        "collapse": "collapse" + str(le),
        "header": header,
        "body": body,
    }


def index_page(request):
    context = {
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


def votings(request):
    context = {
        'pagename': 'Голосования',
        'menu': get_menu_context(),
        'votings': Voting.objects.all(),
    }
    return render(request, 'pages/votings.html', context)


def vote_page(request, vote_id):
    voting = get_object_or_404(Voting, id=vote_id)
    vote_variants = VoteVariant.objects.filter(voting=vote_id)
    vote_facts_variants = []
    current_user = request.user
    is_author = False
    if current_user == voting.author:
        is_author = True

    vote_facts = []
    is_anonymous = current_user.is_anonymous

    allow_vote = True
    view_result = True

    if not is_anonymous:
        vote_facts = VoteFact.objects.filter(user=current_user, variant__voting=voting)
        for i in vote_facts:
            vote_facts_variants.append(i.variant)

    if request.method == 'POST':
        if not is_anonymous:
            vote = request.POST.get("VOTE")
            btn = request.POST.get("CLBTN")
            if btn:
                voting.open = False
                print("Закрыто")
                voting.save()
            if (vote):
                variant = VoteVariant.objects.get(id=vote)
                isexist = VoteFact.objects.filter(user=current_user, variant__voting=voting)  # голосовал ли ранее
                if (not isexist) or voting.type == 2:
                    if not VoteFact.objects.filter(user=current_user, variant=variant).exists():
                        new_vote = VoteFact(user=current_user, variant=variant)
                        new_vote.save()
                        vote_facts_variants.append(new_vote.variant)

    results = VoteFact.objects.filter(variant__voting=voting)
    len_results = len(results)
    result_percents = []

    if len_results != 0:
        for i in vote_variants:
            result_percents.append([i.description, int(len(VoteFact.objects.filter(
                variant=i)) / len_results * 100)])  # процент голосования с 1 знаком после запятой
    else:
        for i in vote_variants:
            result_percents.append([i.description, 0])

    print(result_percents)

    is_open = voting.open

    # for i,j in zip([1,2,3],[4,5,6]):
    # print(i,j)
    if is_anonymous:
        allow_vote = False

    allow_vote = is_open
    view_result = not is_open

    if is_author:
        view_result = True

    types = [
        "Выберите один из двух вариантов ответа",
        "Выберите один из вариантов ответа",
        "Выберите один или несколько вариантов ответа",
    ]

    str_type = types[voting.type]
    context = {
        'pagename': 'Vote page',
        'menu': get_menu_context(),
        'author': voting.author,
        "vote": voting,
        "vote_variants": vote_variants,
        "vote_fact": vote_facts_variants,
        "is_anonymous": is_anonymous,
        "allow_vote": allow_vote,
        "str_type": str_type,
        "type": voting.type,
        "is_author": is_author,
        "view_result": view_result,
        "result_percents": result_percents,
    }
    return render(request, 'pages/vote.html', context)


def profile(request):
    current_user = request.user
    current_user = User.objects.get(id=current_user.id)

    user_votings = Voting.objects.filter(author=current_user)

    context = {
        'pagename': 'Профиль',
        'menu': get_menu_context(),
        'author': current_user,
        'user_votings': user_votings,
    }
    return render(request, 'pages/profile.html', context)


def register(request):
    error_name_alredy_exsist = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and not User.objects.filter(username=form.cleaned_data.get("username")).exists():
            user = User.objects.create_user(form.cleaned_data.get("username"),
                                            form.cleaned_data.get("email"),
                                            form.cleaned_data.get("password"))
            user.first_name, user.last_name = form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")
            user.save()
            return render(request, 'registration/registration_done.html', {'new_user': user})
        else:
            if User.objects.filter(username=form.cleaned_data.get("username")).exists():
                error_name_alredy_exsist = True
            form = UserForm()
    else:
        form = UserForm()

    context = {
        'pagename': 'Регистрация',
        'menu': get_menu_context(),
        'form': form,
        'error_name_alredy_exsist': error_name_alredy_exsist
    }

    return render(request, 'registration/registration.html', context)


@login_required
def add_voting(req):
    context = {
        'menu': get_menu_context()
    }

    if req.method == 'POST':
        votingCreationData = json.loads(req.body.decode('utf-8'))

        if "title" not in votingCreationData or votingCreationData["title"] == "":
            return JsonResponse({'status': 'err', 'description': 'Укажите заголовок голосования!'})

        if "description" not in votingCreationData or votingCreationData["description"] == "":
            return JsonResponse({'status': 'err', 'description': 'Укажите описание голосования!'})

        if "type" not in votingCreationData or votingCreationData["type"] == "":
            return JsonResponse({'status': 'err', 'description': 'Укажите тип голосования!'})

        if "vote_variants" not in votingCreationData or votingCreationData["vote_variants"] == "":
            return JsonResponse({'status': 'err', 'description': 'Не указаны варианты голосования!'})

        for variant in votingCreationData["vote_variants"]:
            if variant == "":
                return JsonResponse({'status': 'err', 'description': 'Не указаны все варианты голосования!'})

        voteType = 0
        if votingCreationData["type"] == "type_one_to_n":
            voteType = 1
        elif votingCreationData["type"] == "type_m_to_n":
            voteType = 2

        newVotingRecord = Voting(
            name=votingCreationData["title"],
            description=votingCreationData["description"],
            type=voteType,
            author=req.user
        )
        newVotingRecord.save()

        voteVariants = votingCreationData["vote_variants"]

        if len(voteVariants) < 2:
            return JsonResponse({'status': 'err', 'description': 'В голосовании должно быть минимум 2 варианта!'})

        if voteType == 0 and len(voteVariants) > 2:
            voteVariants = voteVariants[:2]

        for variant in voteVariants:
            newVoteVariant = VoteVariant(
                voting=newVotingRecord,
                description=variant
            )
            newVoteVariant.save()

        return JsonResponse({'status': 'ok', 'description': 'Голосование успешно создано!',
                             'params': {'voting_id': newVotingRecord.id}})

    return render(req, 'pages/vote_constructor.html', context)
