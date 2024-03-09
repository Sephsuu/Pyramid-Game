from django.shortcuts import render, redirect
from .forms import VoteForm
from .models import Students, Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def validate(request):
    if request.method == 'POST':
        # Retrieve the entered username from the form
        username = request.POST.get('username')

        # Check if a user with the entered username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If a user with the entered username does not exist, display an error message
            messages.error(request, "Invalid username.")
            return redirect('index')  # Replace 'index' with the name of your index URL pattern

        # Log the user in
        login(request, user)
        return redirect('vote')  # Replace 'dashboard' with the name of your dashboard URL pattern

    # If the request method is not POST or if the form has not been submitted, render the HTML template
    return render(request, 'home.html')

def vote(request):
    if request.method == 'POST':
        # Get the surnames of the students the user voted for from the form
        surnames = [
            request.POST.get('recipient_surname_1').upper(),
            request.POST.get('recipient_surname_2').upper(),
            request.POST.get('recipient_surname_3').upper(),
            request.POST.get('recipient_surname_4').upper(),
            request.POST.get('recipient_surname_5').upper(),
        ]
         
        # Get the current user (voter)
        user = request.user.students

        # Check for empty fields
        if any(surname == '' for surname in surnames):
            messages.success(request, "Please complete all fields.")
            return render(request, 'vote.html')

        # Iterate over the surnames to find the corresponding students and create votes
        voted_students = set()  # To keep track of already voted students
        for surname in surnames:
            if surname in voted_students:
                messages.success(request, f"The name '{surname}' is repeated.")
                return render(request, 'vote.html')
            try:
                recipient = Students.objects.get(last_name__iexact=surname)
                # Check if the voter is not voting for themselves
                if recipient != user:
                    vote, created = Vote.objects.get_or_create(voter=user, recipient=recipient)
                    if not created:
                        vote.vote_count += 1
                        vote.save()
                    voted_students.add(surname)
            except Students.DoesNotExist:
                messages.success(request, f"No student found with the last name '{surname}'")

        # Redirect to a success page or back to the voting page
        return redirect('vote_success')  # Change 'dashboard' to the name of your dashboard URL pattern

    return render(request, 'vote.html')

def results(request):
    students = Students.objects.all()
    student_votes = {}

    # Iterate over each student and get their total vote count
    for student in students:
        total_votes = Vote.objects.filter(recipient=student).count()
        student_votes[student] = total_votes

    sorted_students = sorted(student_votes.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'results.html', {'sorted_students': sorted_students})

def vote_success(request):
    return render(request, "vote_success.html", {})
