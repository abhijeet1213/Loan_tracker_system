from django.shortcuts import render
from .models import *
import datetime
from django.utils import timezone
import pytz
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt 
import json
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
@csrf_exempt
def create_record(request):
   
    fmt = '%Y-%m-%d %H:%M:%S'
    # utc = timezone.localtime(timezone.now()).replace(tzinfo=pytz.UTC)
    # localtz = utc.astimezone(timezone.get_current_timezone())

    context={}
    if request.method=='POST':
        if request.POST.get('t_date') and request.POST.get('application_loan_number'):
          
            submitrecord=KserviceRecords()
          
            submitrecord.user_id=request.user.id
            
                       
            submitrecord.t_date= request.POST.get('t_date')
            submitrecord.application_loan_number=request.POST.get('application_loan_number')
            submitrecord.case_status='WIP'
            # print(localtz.strftime(fmt))
            submitrecord.start_time=timezone.now().strftime(fmt)
            submitrecord.save()
            t_date=submitrecord.t_date
            
            data=submitrecord
           
          
            context={
                    
                    'data': data,
                    't_date':t_date

            }

            
            return render(request,'dashboard/edit_record.html',context)
        else:
            return render(request,'dashboard/edit_record.html',context)
@login_required(login_url='/')
@csrf_exempt
def submitrecord(request):
    fmt = '%Y-%m-%d %H:%M:%S'
    # utc = timezone.localtime(timezone.now()).replace(tzinfo=pytz.UTC)
    # localtz = utc.astimezone(timezone.get_current_timezone())
    if request.method=='POST':
        data=dict(json.loads(request.body))
        caseid=data['c_id']
        print(caseid)
        submitrecord=KserviceRecords.objects.get(id=caseid)
        submitrecord.akuser_id=data['akuser_id'] if data['akuser_id']!='' else None
        submitrecord.portfolio_lender=data['portfolio_lender']
        submitrecord.borrower_name=data['borrower_name']
        submitrecord.origination_date=data['origination_date'] if data['origination_date']!='' else None
        submitrecord.maturity_date=data['maturity_date'] if data['maturity_date']!="" else None
        submitrecord.origination_amount=data['origination_amount']
        submitrecord.salesforce_ticket_number=data['salesforce_ticket_number'] if data['salesforce_ticket_number']!='' else None
        submitrecord.business_structure=data['business_structure']
        user=request.user.first_name+" " + request.user.last_name
        time=timezone.now().strftime(fmt)
        submitrecord.comment=data['comment']
        if(data['kore']!=''):
            submitrecord.kore=(data['kore']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        else:
            submitrecord.kore=''
        if(data['inscribe']!=''):
            submitrecord.inscribe=(data['inscribe']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        else:
            submitrecord.kore=''
        if(data['google_search']!=''):
            submitrecord.google_search=(data['google_search']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        else:
            submitrecord.google_search=''
        
        if(data['tlo']!=''):
            submitrecord.tlo=(data['tlo']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        else:
            submitrecord.tlo=''
        submitrecord.case_status='Completed'
        submitrecord.end_time=timezone.now().strftime(fmt)
        submitrecord.save()

       
        msg = "1"
        return HttpResponse(msg)

@login_required(login_url='/')
@csrf_exempt
def updaterecord(request):
    fmt = '%Y-%m-%d %H:%M:%S'
    # utc = timezone.localtime(timezone.now()).replace(tzinfo=pytz.UTC)
    # localtz = utc.astimezone(timezone.get_current_timezone())
    if request.method=='POST':
        data=dict(json.loads(request.body))
        caseid=data['c_id']
        print(caseid)
        submitrecord=KserviceRecords.objects.get(id=caseid)
        submitrecord_read=KserviceRecords.objects.get(id=caseid)

        submitrecord.akuser_id=data['akuser_id'] if data['akuser_id']!='' else None
        submitrecord.portfolio_lender=data['portfolio_lender']
        submitrecord.borrower_name=data['borrower_name']
        submitrecord.origination_date=data['origination_date'] if data['origination_date']!='' else None
        submitrecord.maturity_date=data['maturity_date'] if data['maturity_date']!="" else None
        submitrecord.origination_amount=data['origination_amount']
        submitrecord.salesforce_ticket_number=data['salesforce_ticket_number'] if data['salesforce_ticket_number']!='' else None
        submitrecord.business_structure=data['business_structure']
        user=request.user.first_name+" " + request.user.last_name
        time=timezone.now().strftime(fmt)
        
       
        
        
        

        if( (submitrecord_read.kore=="" or submitrecord_read.kore==None) and data['kore'] !=""):
            submitrecord.kore=(data['kore']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        if ((submitrecord_read.inscribe=="" or submitrecord_read.inscribe==None) and data['inscribe'] !=""):
            submitrecord.inscribe=(data['inscribe']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        if((submitrecord_read.google_search=="" or submitrecord_read.google_search==None )and data['google_search'] !=""):
            submitrecord.google_search=(data['google_search']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        submitrecord.comment=data['comment']
        if((submitrecord_read.tlo=="" or submitrecord_read.tlo==None) and data['tlo'] !=""):
            submitrecord.tlo=(data['tlo']+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
        submitrecord.case_status='Completed'
        submitrecord.end_time=timezone.now().strftime(fmt)
        submitrecord.save()

       
        msg = "1"
        return HttpResponse(msg)

@login_required(login_url='/')
@csrf_exempt
def anlyst_dashboard(request):
    try:
    
        sql="select *from kservice_aap_kservicerecords inner join accounts_customeuser on accounts_customeuser.id=kservice_aap_kservicerecords.user_id where case_status='Completed' ;"
        data=list(KserviceRecords.objects.raw(sql))
        context = {'data': data}
        html_template = loader.get_template('dashboard/analyst_dashboard.html')
        return HttpResponse(html_template.render(context, request))
    except Exception as e:
        print(e)
        return HttpResponse(html_template.render(context, request))
    return render(request, 'dashboard/analyst_dashboard.html')

@csrf_exempt
@login_required(login_url='/')

def manual_entry(request):

    if request.user.is_authenticated:

        data= KserviceRecords.objects.filter(user_id=request.user.id,case_status="WIP")
        # for i in data:
            
        context = {'data': data
                    }
        html_template = loader.get_template('dashboard/new_record.html')
        return HttpResponse(html_template.render(context, request))
    

@login_required(login_url='/')
@csrf_exempt
def update_comment(request):
    try:
        fmt = '%Y-%m-%d %H:%M:%S'
        data=dict(json.loads(request.body))
        id=data['id']
        commnet=data['comment']
        case_id=data['case_id']

        submitrecord=KserviceRecords.objects.get(id=case_id)
        if(data['comment']==""):
            msg = "1"
            return HttpResponse(msg)
        if(id=='KORE'):
            old_str=submitrecord.kore
            if old_str=="" or old_str==None:
                old_str=''
            user=request.user.first_name+" " + request.user.last_name
            time=timezone.now().strftime(fmt)
            value=(old_str+"\n"+commnet+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
            KserviceRecords.objects.filter(id=case_id).update(kore=value)
        if(id=='Inscribe'):
            old_str=submitrecord.inscribe
            if old_str=="" or old_str==None:
                old_str=''
            user=request.user.first_name+" " + request.user.last_name
            time=timezone.now().strftime(fmt)
            value=(old_str+"\n"+commnet+" | "+" Creation Date : "+time +" Created By : " +user +"\n")
            KserviceRecords.objects.filter(id=case_id).update(inscribe=value)
        if(id=='Google Search'):
            old_str=submitrecord.google_search
            if old_str=="" or old_str==None:
                old_str=''
            user=request.user.first_name+" " + request.user.last_name
            time=timezone.now().strftime(fmt)
            value=(old_str+"\n"+commnet+" | "+" Creation Date : "+time +" Created By : " +user+"\n" )

            KserviceRecords.objects.filter(id=case_id).update(google_search=value)
        if(id=='TLO'):
            old_str=submitrecord.tlo
            if old_str=="" or old_str==None:
                old_str=''
            user=request.user.first_name+" " + request.user.last_name
            time=timezone.now().strftime(fmt)
            value=(old_str+"\n"+commnet+" | "+" Creation Date : "+time +" Created By : " +user+"\n" )

            KserviceRecords.objects.filter(id=case_id).update(tlo=value)
        msg = "1"
        return HttpResponse(msg)
    except Exception as e:
        print(e)
        msg = "2"
        return HttpResponse(msg)

@login_required(login_url='/')
@csrf_exempt
def view_record(request,id):

       
            

    if request.user.is_authenticated:
            data= KserviceRecords.objects.get(id=id)
            org_date=data.origination_date
           
            maturity_date=data.maturity_date  
            context = {'data': data,
                'org_date':org_date,
                'maturity_date':maturity_date}

               
            html_template = loader.get_template('dashboard/edit_record.html')
            return HttpResponse(html_template.render(context, request))




@login_required(login_url='/')
@csrf_exempt
def view_record_(request,id):

       
            

    if request.user.is_authenticated:
            data= KserviceRecords.objects.get(id=id)
            org_date=data.origination_date
           
            maturity_date=data.maturity_date  
            context = {'data': data,
                'org_date':org_date,
                'maturity_date':maturity_date}

               
            html_template = loader.get_template('dashboard/updaterecords.html')
            return HttpResponse(html_template.render(context, request))

@login_required(login_url='/')
@csrf_exempt
def report_dashboard(request):

    
    return render(request,'dashboard/reports.html')

@login_required(login_url='/')
@csrf_exempt
def generate_report(request):
    
   
    fromdate=request.POST.get('from_date')
    todate=request.POST.get('to_date')
    dollar_amount=request.POST.get('d_amount')
      

    if dollar_amount=="":
        sqlquery='''Select *from kservice_aap_kservicerecords
        inner join accounts_customeuser on accounts_customeuser.id=kservice_aap_kservicerecords.user_id
        where kservice_aap_kservicerecords.case_status="Completed" and kservice_aap_kservicerecords.t_date between "''' + fromdate + '''" and "''' + todate +'''"'''
    elif fromdate !="" and todate != ""  and dollar_amount != "":
        sqlquery='''Select *from kservice_aap_kservicerecords
        inner join accounts_customeuser on accounts_customeuser.id=kservice_aap_kservicerecords.user_id
        where kservice_aap_kservicerecords.case_status="Completed" and kservice_aap_kservicerecords.t_date between "''' + fromdate + '''" and "'''+ todate +'''" and ''' + '''origination_amount = "''' + dollar_amount +'''"'''
    elif fromdate =="" and todate == ""  and dollar_amount != "":

                sqlquery='''Select *from kservice_aap_kservicerecords
        inner join accounts_customeuser on accounts_customeuser.id=kservice_aap_kservicerecords.user_id
        where kservice_aap_kservicerecords.case_status="Completed" and origination_amount = "''' + dollar_amount +'''"'''

    data = KserviceRecords.objects.raw(sqlquery)
    for i in data:
        i.duration=i.end_time-i.start_time
        
    context={'data':data}
    
    # html_template = loader.get_template('dashboard/reports.html')
    # return HttpResponse(html_template.render(context, request))
    html_template = render_to_string('dashboard/rts_report.html', context)  
    return JsonResponse({'string':html_template})