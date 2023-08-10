from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from admission.models import Student


@login_required(login_url="/admission/login")
def index(request, index_no):
    student = Student.objects.get(index_number=index_no)
    fname = student.first_name
    context = {
        'fname': fname,
        'student': student
    }

    if request.method == "POST":
        return redirect('admission:generate_pdf', index_no)

    return render(request, 'user/index.html', context)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!!")
            return redirect('admission:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!!")
            return redirect('admission:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('admission:signup')

        if not pass1.isalnum():
            messages.error(request, "Password must contain both letters and numbers")
            return redirect('admission:signup')

        if len(pass1) < 7:
            messages.error(request, "Password must contain at least 8 characters")
            return redirect('admission:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True

        myuser.save()

        messages.success(request, "Your Account has been created successfully. \n ")
        messages.success(request, "We have sent you a confirmation link to your email. \n ")
        messages.success(request, "Please click on it to activate your account. \n ")

        return redirect('admission:login')

    return render(request, 'auth/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        index_no = pass1

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('admission:index', index_no)

        else:
            messages.error(request, "Username or Password is incorrect")

    return render(request, 'auth/login.html')


@login_required
def log_out(request):
    logout(request)
    return render(request, 'auth/logout.html')


def generate_pdf(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/letterhead.png"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    index = mystudent.index_number
    fname = mystudent.first_name
    middlename = mystudent.middle_name
    sname = mystudent.surname
    box_no = mystudent.box_no
    box_code = mystudent.box_code
    town = mystudent.town
    country = mystudent.country
    email = mystudent.email_address
    fee_day = mystudent.fee_day
    fee_boarder = mystudent.fee_boarder
    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    mode = mystudent.mode
    course = mystudent.course

    content = [logo_img, letterhead_img]

    date_text = "5th August 2021"
    date = Paragraph(date_text, styles['Letter'])
    content.append(date)

    index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, styles['Letter2'])
    content.append(indexno)

    full_name_text = fname + " " + middlename + " " + sname
    full_name = Paragraph(full_name_text, styles['Heading4'])
    content.append(full_name)

    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])
    content.append(post)

    post_code_text = town + " , " + country
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, styles['Blank'])
    content.append(blank)

    mobile_text = "Mobile No: " + num1 + " " + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2021/2022 ACADEMIC YEAR (SEPTEMBER 2021 INTAKE)"
    title = Paragraph(title_text, styles['Title'])
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission to the Institute, I am pleased to offer you a place " \
                      "at Kenya Institute of Mass Communication as a " + mode + " Student for a course leading " \
                                                                                "to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    line2_text = "_______________________________________________________________________________"
    line2 = Paragraph(line2_text, styles['Line'])

    title2_text = "PGD/DIP/CERT IN: " + course
    title2 = Paragraph(title2_text, styles['Heading4'])
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Week Days: - Monday – Friday (8.00am – 4.00pm), " \
                      "at our Main Campus, Nairobi, and will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on ___________________________________________, during working" \
                      "Hours, between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the " \
                      "Acceptance Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be " \
                      "_______________________________."
    paragraph3 = Paragraph(paragraph3_text, styles['Normal'])
    content.append(paragraph3)
    content.append(blank)

    paragraph4_text = "However, this admission is subject to satisfactory verification of your academic documents by " \
                      "the KIMC authorities & KNEC. Please bring your ORIGINAL & COPIES of the K.C.S.E. " \
                      "Certificate/Results Slips, KCPE Certificate, School Leaving Certificate, National ID, " \
                      "& Birth Certificate, during registration. Download and fill the following admission packages (" \
                      "forms) that are available on our website: www.kimc.ac.ke, e-resources section. Please bring " \
                      "them during the reporting the day."
    paragraph4 = Paragraph(paragraph4_text, styles['Normal'])
    content.append(paragraph4)
    content.append(blank)

    list_item1_text = "Acceptance Form, KIMC/KAB/ADM 02"
    list1_item1 = (Paragraph(list_item1_text, styles['Normal'], bulletText='i)'))
    content.append(list1_item1)

    list_item2_text = "Admission Forms, KIMC/KAB/ADM 003"
    list1_item2 = (Paragraph(list_item2_text, styles['Normal'], bulletText='ii)'))
    content.append(list1_item2)

    list_item3_text = "Medical Form, KIMC/KAB/ADM 004"
    list1_item3 = (Paragraph(list_item3_text, styles['Normal'], bulletText='iii)'))
    content.append(list1_item3)

    list_item4_text = "Students Rules & Regulations, KIMC/KAB/ADM 0005"
    list1_item4 = (Paragraph(list_item4_text, styles['Normal'], bulletText='iv)'))
    content.append(list1_item4)

    list_item5_text = "Hostel Application Form, KIMC/KAB/ADM 006 (Optional)"
    list1_item5 = (Paragraph(list_item5_text, styles['Normal'], bulletText='v)'))
    content.append(list1_item5)

    paragraph5_text = "The Institute is located along   Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former Kenya Bus Service " \
                      "stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, styles['Heading4'])
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "Requirements:"
    no1 = Paragraph(no1_text, styles['Number'])
    paragraph6 = Paragraph(paragraph6_text, styles['Normal_indent'])
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, styles['Normal_indent'],
                                            bulletText='            a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, styles['Normal_indent'],
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation"
    no2 = Paragraph(no2_text, styles['Number'])
    paragraph7 = Paragraph(paragraph7_text, styles['Normal_indent'])
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)

    paragraph7_text_list_item1_text = "Application: KIMC provides limited accommodation on first come first serve " \
                                      "basis. If interested, please apply DIRECTLY using the attached Hostel " \
                                      "Application Form."
    paragraph7_text_list_item1 = (Paragraph(paragraph7_text_list_item1_text, styles['Normal_indent'],
                                            bulletText='            a)'))
    content.append(paragraph7_text_list_item1)

    paragraph7_text_list_item2_text = "Boarders: Boarders MUST bring enough personal effects - Toiletries, " \
                                      "Two Bed sheets, One Towel, Two Blankets, One Bedcover, Mosquito Net, " \
                                      "One Pillow & Two Pillowcases, One Mug, One Melamine Dinner Plate and" \
                                      "One Table spoon.  Please KIMC does not provide a Special Diet."
    paragraph7_text_list_item2 = (Paragraph(paragraph7_text_list_item2_text, styles['Normal_indent'],
                                            bulletText='            b)'))
    content.append(paragraph7_text_list_item2)

    paragraph7_text_list_item3_text = "The Institute does not allow use of ANY electrical appliances (kettle, " \
                                      "emersion heater, shower). If caught, you will be surcharged and when repeated " \
                                      "lose you boarding status."
    paragraph7_text_list_item3 = (Paragraph(paragraph7_text_list_item3_text, styles['Normal_indent'],
                                            bulletText='            c)'))
    content.append(paragraph7_text_list_item3)
    content.append(blank)

    no3_text = "3."
    paragraph8_text = "Fee Structure"
    no3 = Paragraph(no3_text, styles['Number'])
    paragraph8 = Paragraph(paragraph8_text, styles['Normal_indent'])
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Fees: KIMC Fees is paid ANNUALLY but NOT termly and is payable either Once, " \
                                      "OR in Three (3) Instalments - Half (1/2) at the start of each year and the " \
                                      "balance is payable in Two (2) Equal Instalments."
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, styles['Normal_indent'],
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)

    paragraph8_text_list_item2_text = "The Institute fees and charges are as below but subject to review:"
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, styles['Normal_indent'],
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)
    content.append(blank)

    table_data = [
        ['No.', 'Fees', '', 'Amount Payable (Ksh.)', '', ''],
        ['', '', '', 'Year One(1)', 'Year Two(2)', 'Year Three(3)'],
        ['1', 'Registration Fees', '', '1,000.00', '-', '-'],
        ['2', 'Tuition Fees', 'Boarders', '96,000.00', '94,000.00', '94,000.00'],
        ['', '', 'Day Scholars', '84,900.00', '82,900.00', '82,900.00'],
        ['3', 'KNEC Examination (Engineering)', '', '9,600.00', '8,250.00', '10,050.00'],
        ['4', 'Industrial Attachment (Optional)', '', '8,100.00', '-', '-']
    ]
    table = Table(table_data)
    table_styling = TableStyle([
        ('BACKGROUND', (0, 0), (6, 1), colors.gray),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (2, 1)),
        ('SPAN', (3, 0), (5, 0)),
        ('SPAN', (0, 3), (0, 4)),
        ('SPAN', (1, 3), (1, 4)),
        ('SPAN', (1, 5), (2, 5)),
        ('SPAN', (1, 6), (2, 6)),
        ('INNERGRID', (0, 0), (6, 6), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ])
    table.setStyle(table_styling)
    content.append(table)
    content.append(blank)

    paragraph8_text_list_item3_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENT, AGENT BANKING OR " \
                                      "INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute of Mass " \
                                      "Communication, Kenya Commercial Bank (KCB), KICC Branch, Account No. 1143 244 " \
                                      "362, OR KCB Paybill: 522522, Account: 1143 244 362, and indicate the MPESA " \
                                      "Transaction Number on the Admission Form. Please note that fees once paid is " \
                                      "NOT refundable or transferable."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, styles['Normal_indent'],
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    paragraph8_text_list_item4_text = "HELB. Needy students may apply for HELB Loan. To apply, visit HELB " \
                                      "website on www.helb.co.ke or their Offices at Anniversary Towers, Nairobi."
    paragraph8_text_list_item4 = (Paragraph(paragraph8_text_list_item4_text, styles['Normal_indent'],
                                            bulletText='            d)'))
    content.append(paragraph8_text_list_item4)
    content.append(blank)

    no4_text = "4."
    paragraph9_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                      "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                      "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, styles['Number'])
    paragraph9 = Paragraph(paragraph9_text, styles['Normal_indent'])
    content.append(no4)
    content.append(paragraph9)
    content.append(blank)

    no5_text = "5."
    paragraph10_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, styles['Number'])
    paragraph10 = Paragraph(paragraph10_text, styles['Normal_indent'])
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, styles['Number'])
    paragraph11 = Paragraph(paragraph11_text, styles['Normal_indent'])
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)

    paragraph13_text = "PETER WAKOLI"
    paragraph13 = Paragraph(paragraph13_text, styles['Heading5'])
    content.append(paragraph13)

    paragraph14_text = "AG. DIRECTOR/CEO"
    paragraph14 = Paragraph(paragraph14_text, styles['Heading5'])
    content.append(paragraph14)

    doc.build(content)
    return response
