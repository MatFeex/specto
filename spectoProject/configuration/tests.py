def vmq_planning(request):
    vmq_planning = VMQ_Planning.objects.all().order_by('-year')
    return render(request,'configuration/planning/vmq/vmq_planning.html',{'vmq_planning':vmq_planning})


def create_vmq_planning(request):

    if request.method == 'POST':

        # GET PLANNING DATES
        month = request.POST.get('month')
        year = request.POST.get('year')

        # delete previous planning one the same period
        VMQ_Planning.objects.filter(month=month,year=year).delete()

        # GET employees QUALIFIED
        employees_qualified = Qualification.objects.filter(vmq_qualification=True).values_list('employee', flat=True)
        count_qualified = employees_qualified.count()
        
        # GET employees already VISITED
        vms_employee_visited = VMQ_Planning.objects.filter(closed=True).values_list('vms_employee_visited', flat=True)

        # # GET employees NOT VISITED
        employee_not_visited = Employee.objects.exclude(matricule__in=vms_employee_visited).values_list('matricule', flat=True)
        count_not_visited = employee_not_visited.count()
        print(vms_employee_visited)
        print(employee_not_visited)

        
        # if NB Employees To Visit >= NB Employees Qualified * 2 --> Next visited are only in Employee database
        if count_not_visited >= count_qualified*2 : 
            employee_to_be_visited = employee_not_visited[:count_qualified*2]
       
        else : # if NB Employees To Visit < NB Employees Qualified * 2 --> Next visited are the ones in Employee database + The first ones already visited
            employees = Employee.objects.values_list('matricule', flat=True) 
            employee_to_be_visited = employee_not_visited + employees
            employee_to_be_visited = employee_to_be_visited[:count_qualified*2]


        zip_list = dict( zip(employee_to_be_visited, cycle(employees_qualified)) if len(employee_to_be_visited) > len(employees_qualified) else zip(cycle(employee_to_be_visited), employees_qualified))

        # for vms_employee_qualified in employees_qualified : 
        for visited,user in zip_list.items() : 
            form = VMQ_PlanningForm().save(commit=False)
            form.vms_employee_qualified_id = user
            form.vms_employee_visited_id = visited
            form.month = month
            form.year = year
            form.save()

        return redirect('vmq-planning')
        
    return render(request,'configuration/planning/vmq/vmq_planning_date.html')
