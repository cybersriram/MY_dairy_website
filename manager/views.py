from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
import time,datetime,calendar,sqlite3
# Create your views here.
def index(request):
    return render(request,"main.html")
def login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['psw']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,"main.html")
        else:
            return render(request,"index.html",{'temp':5})
    else:
        return render(request,"index.html")
def register(request):
    try:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['Email']
            password = request.POST['psw']
            fullname = request.POST['fname'] 
            repass = request.POST['psw-repeat']
            if password == repass:
                user = User.objects.create_user(username=name,password=password,email=email,first_name=fullname)
                user.save()
                create_db(name)
                return render(request,"index.html")
            else:
                return render(request,"register.html",{'t1':'Password Doesnot Match','temp':1})
    except:
        temp = 1
        time.sleep(6)
        return render(request,"register.html",{'t':temp})
        
    else:
        return render(request,"register.html")
def logout(request):
    auth.logout(request)
    return render(request,"main.html")
def create_db(table_name):
    #Connecting to sqlite
    conn = sqlite3.connect('manager.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    sql = "CREATE TABLE "+table_name+"( SLNO INT, Date CHAR(11), DAY  CHAR(11),CONTENT CHAR(1000),PRIMARY KEY(Date))"
        #Creating table as per requirement
    cursor.execute(sql)
    print("Table created successfully........")

        # Commit your changes in the database
    conn.commit()

        #Closing the connection
    conn.close()
def findDay(date): 
    born = datetime.datetime.strptime(date, '%m/%d/%Y').weekday() 
    return (calendar.day_name[born])
def entry(request):
    if request.method == "POST":
        date = request.POST['date']
        content = request.POST.get('text')
        day = findDay(date)
        name = request.user.username
        #Connecting to sqlite
        conn = sqlite3.connect('manager.db')

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        
        sql = "INSERT INTO "+name+"(SLNO, Date, DAY, CONTENT) VALUES (?, ?, ?, ?)"
        # Preparing SQL queries to INSERT a record into the database.
        sql2 = "select count(*) from "+name
        cursor.execute(sql2)
        t = cursor.fetchone()
        t = int(t[0])+1 
        cursor.execute(sql,(t,date,day,content))
        # Commit your changes in the database
        conn.commit()
        # Closing the connection
        conn.close()
        return redirect("main")
    else:
        return render(request,"entry.html")
def display(request):
    if request.method == "POST":
        From = request.POST['from']
        name = request.user.username
        res = fetch_db(name,From)
        From = datetime.datetime.strptime(From,'%m/%d/%Y')
        #for i in  range(day.days+1):
        return render(request,"con_display.html",{'day':res[0][0],'content':res[0][1]})
    else:
        return render(request,"display.html")
def fetch_db(name,FROM):
    FROM = "'"+FROM+"'"
    conn = sqlite3.connect('manager.db')

        #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
        
    sql = "SELECT DAY,CONTENT FROM "+name+" WHERE Date = "+FROM
        # Preparing SQL queries to INSERT a record into the database.
    cursor.execute(sql)
        # Commit your changes in the database
    result = cursor.fetchall()

        # Closing the connection
    conn.close()
    return result