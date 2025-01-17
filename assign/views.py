from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project

@login_required
def assign_project(request):
    if request.method == "POST":
        project_name = request.POST.get("project_name")
        employee_id = request.POST.get("employee_id")
        assignment_details = request.POST.get("assignment_details")

        if project_name and employee_id:
            try:
                employee = get_object_or_404(User, id=employee_id)
                Project.objects.create(
                    project_name=project_name,
                    user=employee,
                    project_assign=assignment_details
                )
                return redirect("assign_project")
            except Exception as e:
                return render(request, "assign.html", {"error": str(e)})

    employees = User.objects.filter(is_staff=False)  # Assuming non-staff are employees
    projects = Project.objects.select_related("user").all()  # Optimize query with select_related
    return render(request, "assign.html", {
        "employees": employees,
        "projects": projects
    })


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect("assign_project")