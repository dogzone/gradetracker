from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
#cross-site request forgery --> method for people hacking into website
from GradeTracker.models import Student, Course, Graded_Activities, SubGraded_Activities, Templates
from GradeTracker.forms import courseAdd, activityAdd, activityEdit, subactivityAdd, MyRegistrationForm
from django.contrib.auth.decorators import login_required

@login_required
def editGradedActivity( request, activity_id=None ):
    
    ##Grab the student from the user object, if there is none return invalid login
    try:
        student = Student.objects.filter(user=request.user)[0]
    except: 
        return render(request, 'GradeTracker/invalid_login.html')

    activity = get_object_or_404( Graded_Activities, pk=activity_id ) #Get the Graded_Activity to edit

    if request.method == 'POST': 			# If the form has been submitted...
        form = activityEdit(request.POST, instance=activity) # A form bound to the POST data, with the activity loaded
        if form.is_valid(): 				# All validation rules pass
            # Process the data in form.cleaned_data
            form.save()

            return HttpResponseRedirect('/GT/' + str(student.id) +'/' + str(activity.course.id)  + '/' ) # Redirect after POST
    else:
        form = activityEdit(instance=activity) # An unbound form
    return render(request, 'GradeTracker/editActivity.html', { 'form': form , 'activity':activity} )

@login_required
def deleteGradedActivity( request, activity_id):
    student = Student.objects.filter(user=request.user)[0]
    activity = get_object_or_404( Graded_Activities, pk=activity_id ) #Get the Graded_Activity to delete
    courseReturned = activity.course
    activity.delete()
    return HttpResponseRedirect('/GT/' + str(courseReturned.student.id) +'/' + str(courseReturned.id)  + '/' )
