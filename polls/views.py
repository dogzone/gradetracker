# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.shortcuts import render, get_object_or_404

from polls.models import Question, Choice

def index( request ):
	latest_poll_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_poll_list': latest_poll_list}
	return render(request, 'polls/index.html', context)

def detail( request, poll_id):
	return HttpResponse( "You're looking at poll {} ".format( poll_id ) )

def results( request, poll_id):
	return HttpResponse( "You're looking at results of poll {} ".format( poll_id ) )

def vote(request, poll_id):
    p = get_object_or_404(Question, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
