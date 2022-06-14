from django.shortcuts import redirect, render
from django.http import HttpResponse

from main.modules.db_moodle_requests import get_gits_answers,get_assigns
from main.modules.plagiarism_check import get_plagiarism_result_data
from main.modules.screenshots_compare import get_match_points_and_diff_screen

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        assigns = get_assigns(2)
        return render(request, 'home.html',{'assigns':assigns})
    else:
        return redirect("login")

def assigns(request):
    if (request.GET.get('assign_id')):
        assign_id = request.GET.get('assign_id')
        assign_id = int(assign_id)
        answers = get_gits_answers(2,assign_id)
        exist_a = len(answers)

        return render(request,'assign.html',{'answers': answers, 'exist_a': exist_a, 'assign_id': assign_id})
    else:
        return redirect('/')

def plagiarism_answers(request):
    if (request.GET.get('assign_id')):
        assign_id = request.GET.get('assign_id')
        answers = get_gits_answers(2,assign_id)
        results_of_checking = get_plagiarism_result_data(answers)
        sorted_res = list(results_of_checking)
        sorted_res.sort(key=lambda x: (-x[2],x[1],x[0]))

        return render(request,'antiplagiarism.html',{'results_of_checking': sorted_res})
    else:
        return redirect('/')
        
def screen_test(request):
    if (request.GET.get('answer_url') and request.GET.get('answer_firstname') and request.GET.get('answer_lastname') ):
        url = request.GET.get('answer_url')
        firstname = request.GET.get('answer_firstname')
        lastname = request.GET.get('answer_lastname')
        img_a,img_b,img_diff,percentage_of_diff = get_match_points_and_diff_screen(url)
        match_point_res = (1 - percentage_of_diff)*100
        match_point_res = round(match_point_res)
        return render(request,'compare.html',{'url':url,'firstname':firstname,'lastname':lastname, 'res':match_point_res})
    else:
        return redirect("/")


    
# def home(request):
#     if request.user.is_authenticated:
        
#         # usernames,stud_urls = get_gits_urls(2,1)
#         return HttpResponse("<h1>"+str(usernames)+"</h1>")
#     else:
#         return redirect('/')
