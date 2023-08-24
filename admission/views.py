from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, _baseFontNameB
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from reportlab.lib.pagesizes import A4
from django.contrib.auth import logout
from django.http import HttpResponse
from admission.models import Student
from django.contrib import messages
from reportlab.lib import colors


@login_required(login_url="/admission/login")
def index(request, index_no):
    student = Student.objects.get(index_number=index_no)
    fname = student.first_name
    mode = student.mode

    context = {
        'fname': fname,
        'student': student
    }

    if request.method == "POST":
        if mode == "KUCCPS":
            return redirect('admission:generate_pdf_kuccps', index_no)
        elif mode == "INTERNAL":
            return redirect('admission:generate_pdf_internal', index_no)
        elif mode == "POSTGRAD":
            return redirect('admission:generate_pdf_postgrad', index_no)
        elif mode == "CERTIFICATE":
            return redirect('admission:generate_pdf_certificate', index_no)
        elif mode == "EVENING":
            return redirect('admission:generate_pdf_evening', index_no)
        elif mode == "UPGRADING":
            return redirect('admission:generate_pdf_upgrading', index_no)
        else:
            return redirect('admission:generate_pdf_eldoret', index_no)

    return render(request, 'user/index.html', context)


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


def generate_pdf_kuccps(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

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

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    mode = mystudent.mode
    paragraph1_text = "Following your application through Kenya Universities and Colleges Placement Services (KUCCPS) " \
                      "for admission into the Institute, I am pleased to offer you a place at Kenya Institute of Mass " \
                      "Communication as a REGULAR Student for a course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    line2_text = "_______________________________________________________________________________"
    line2 = Paragraph(line2_text, line_style)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Week Days: - Monday – Friday (8.00am – 4.00pm), " \
                      "at our Main Campus, Nairobi, and will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)

    paragraph7_text_list_item1_text = "Application: KIMC provides limited accommodation on first come first serve " \
                                      "basis. If interested, please apply DIRECTLY using the attached Hostel " \
                                      "Application Form."
    paragraph7_text_list_item1 = (Paragraph(paragraph7_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph7_text_list_item1)

    paragraph7_text_list_item2_text = "Boarders: Boarders MUST bring enough personal effects - Toiletries, " \
                                      "Two Bed sheets, One Towel, Two Blankets, One Bedcover, Mosquito Net, " \
                                      "One Pillow & Two Pillowcases, One Mug, One Melamine Dinner Plate and " \
                                      "One Table spoon.  Please KIMC does not provide a Special Diet."
    paragraph7_text_list_item2 = (Paragraph(paragraph7_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph7_text_list_item2)

    paragraph7_text_list_item3_text = "The Institute does not allow use of ANY electrical appliances (kettle, " \
                                      "emersion heater, shower). If caught, you will be surcharged and when repeated " \
                                      "lose you boarding status."
    paragraph7_text_list_item3 = (Paragraph(paragraph7_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph7_text_list_item3)
    content.append(blank)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees: The Institute fees and charges are as below but subject " \
                                      "to review:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
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
    table.setStyle(table_styling)
    content.append(table)
    content.append(blank)

    paragraph8_text = "NB: Fees apply to each academic year which comprises of three terms " \
                      "including attachment period."
    paragraph8 = Paragraph(paragraph8_text, styles['Normal'])
    content.append(paragraph8)
    content.append(blank)

    paragraph8_text_list_item2_text = "For Boarders:"
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.49,000 (that includes registration fees of " \
                                        "Kshs.1,000 payable during registration)."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)
    content.append(blank)

    paragraph8_text_list_item2_2_text = "Term II: Kshs.24,000 payable at the beginning of Term 2."
    paragraph8_text_list_item2_2 = (Paragraph(paragraph8_text_list_item2_2_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_2)
    content.append(blank)

    paragraph8_text_list_item2_3_text = "Term III: Kshs.24,000 payable at the beginning of Term 3."
    paragraph8_text_list_item2_3 = (Paragraph(paragraph8_text_list_item2_3_text, normal_indent2_style,
                                              bulletText='            iii)'))
    content.append(paragraph8_text_list_item2_3)
    content.append(blank)

    paragraph8_text_list_item3_text = "For Day scholars:"
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    paragraph8_text_list_item3_1_text = "Term I: Kshs.43,450 (that includes registration " \
                                        "fees of Kshs.1,000 payable during registration)."
    paragraph8_text_list_item3_1 = (Paragraph(paragraph8_text_list_item3_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item3_1)
    content.append(blank)

    paragraph8_text_list_item3_2_text = "Term II: Kshs.21,225 payable at the beginning of Term 2."
    paragraph8_text_list_item3_2 = (Paragraph(paragraph8_text_list_item3_2_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item3_2)
    content.append(blank)

    paragraph8_text_list_item3_3_text = "Term III: Kshs.21,225 payable at the beginning of Term 3."
    paragraph8_text_list_item3_3 = (Paragraph(paragraph8_text_list_item3_3_text, normal_indent2_style,
                                              bulletText='            iii)'))
    content.append(paragraph8_text_list_item3_3)
    content.append(blank)

    paragraph9_text_list_item3_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING OR " \
                                      "INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute of Mass " \
                                      "Communication, Kenya Commercial Bank (KCB), KICC Branch, Account No. 1143 244 " \
                                      "362. Please note that fees once paid is NOT refundable or transferable."
    paragraph9_text_list_item3 = (Paragraph(paragraph9_text_list_item3_text, normal_indent_style,
                                            bulletText='            d)'))
    content.append(paragraph9_text_list_item3)

    paragraph10_text_list_item4_text = "HELB: Needy students may apply for HELB Loan. To apply, visit HELB website " \
                                       "on www.helb.co.ke or their Offices at Anniversary Towers, Nairobi. Use the " \
                                       "Serial Number (S.No.) on the first page of this letter in place of Admission " \
                                       "No. when applying for HELB Loan."
    paragraph10_text_list_item4 = (Paragraph(paragraph10_text_list_item4_text, normal_indent_style,
                                             bulletText='            e)'))
    content.append(paragraph10_text_list_item4)
    content.append(blank)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_internal(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

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

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer " \
                      "you a place at the Kenya Institute of Mass Communication as a REGULAR Student for " \
                      "a course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    line2_text = "_______________________________________________________________________________"
    line2 = Paragraph(line2_text, line_style)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Week Days: - Monday – Friday (8.00am – 4.00pm), " \
                      "at our Main Campus, Nairobi, and will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)

    paragraph7_text_list_item1_text = "Application: KIMC provides limited accommodation on first come first serve " \
                                      "basis. If interested, please apply DIRECTLY using the attached Hostel " \
                                      "Application Form."
    paragraph7_text_list_item1 = (Paragraph(paragraph7_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph7_text_list_item1)

    paragraph7_text_list_item2_text = "Boarders: Boarders MUST bring enough personal effects - Toiletries, " \
                                      "Two Bed sheets, One Towel, Two Blankets, One Bedcover, Mosquito Net, " \
                                      "One Pillow & Two Pillowcases, One Mug, One Melamine Dinner Plate and " \
                                      "One Table spoon.  Please KIMC does not provide a Special Diet."
    paragraph7_text_list_item2 = (Paragraph(paragraph7_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph7_text_list_item2)

    paragraph7_text_list_item3_text = "The Institute does not allow use of ANY electrical appliances (kettle, " \
                                      "emersion heater, shower). If caught, you will be surcharged and when repeated " \
                                      "lose you boarding status."
    paragraph7_text_list_item3 = (Paragraph(paragraph7_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph7_text_list_item3)
    content.append(blank)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees: The Institute fees and charges are as below but subject " \
                                      "to review:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
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
    table.setStyle(table_styling)
    content.append(table)
    content.append(blank)

    paragraph8_text = "NB: Fees apply to each academic year which comprises of three terms " \
                      "including attachment period."
    paragraph8 = Paragraph(paragraph8_text, styles['Normal'])
    content.append(paragraph8)
    content.append(blank)

    paragraph8_text_list_item2_text = "For Boarders:"
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.49,000 (that includes registration fees of " \
                                        "Kshs.1,000 payable during registration)."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)
    content.append(blank)

    paragraph8_text_list_item2_2_text = "Term II: Kshs.24,000 payable at the beginning of Term 2."
    paragraph8_text_list_item2_2 = (Paragraph(paragraph8_text_list_item2_2_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_2)
    content.append(blank)

    paragraph8_text_list_item2_3_text = "Term III: Kshs.24,000 payable at the beginning of Term 3."
    paragraph8_text_list_item2_3 = (Paragraph(paragraph8_text_list_item2_3_text, normal_indent2_style,
                                              bulletText='            iii)'))
    content.append(paragraph8_text_list_item2_3)
    content.append(blank)

    paragraph8_text_list_item3_text = "For Day scholars:"
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    paragraph8_text_list_item3_1_text = "Term I: Kshs.43,450 (that includes registration " \
                                        "fees of Kshs.1,000 payable during registration)."
    paragraph8_text_list_item3_1 = (Paragraph(paragraph8_text_list_item3_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item3_1)
    content.append(blank)

    paragraph8_text_list_item3_2_text = "Term II: Kshs.21,225 payable at the beginning of Term 2."
    paragraph8_text_list_item3_2 = (Paragraph(paragraph8_text_list_item3_2_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item3_2)
    content.append(blank)

    paragraph8_text_list_item3_3_text = "Term III: Kshs.21,225 payable at the beginning of Term 3."
    paragraph8_text_list_item3_3 = (Paragraph(paragraph8_text_list_item3_3_text, normal_indent2_style,
                                              bulletText='            iii)'))
    content.append(paragraph8_text_list_item3_3)
    content.append(blank)

    paragraph9_text_list_item3_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING OR " \
                                      "INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute of Mass " \
                                      "Communication, Kenya Commercial Bank (KCB), KICC Branch, Account No. 1143 244 " \
                                      "362. Please note that fees once paid is NOT refundable or transferable."
    paragraph9_text_list_item3 = (Paragraph(paragraph9_text_list_item3_text, normal_indent_style,
                                            bulletText='            d)'))
    content.append(paragraph9_text_list_item3)

    paragraph10_text_list_item4_text = "HELB: Needy students may apply for HELB Loan. To apply, visit HELB website " \
                                       "on www.helb.co.ke or their Offices at Anniversary Towers, Nairobi. Use the " \
                                       "Serial Number (S.No.) on the first page of this letter in place of Admission " \
                                       "No. when applying for HELB Loan."
    paragraph10_text_list_item4 = (Paragraph(paragraph10_text_list_item4_text, normal_indent_style,
                                             bulletText='            e)'))
    content.append(paragraph10_text_list_item4)
    content.append(blank)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_postgrad(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at the Kenya Institute of Mass Communication as a SELF – SPONSORED Student for " \
                      "a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Evening sand Weekends: - Monday – Friday " \
                      "(4.30 pm – 8.30pm) & Saturdays (8.00am – 4.00pm), at our Main Campus, Nairobi. " \
                      "It will take One (1) Academic Year."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "NB: Please note that upon successful completion of the certificate course, you will be " \
                      "eligible for re-admission into a two (2) year Upgrading Diploma but upon application."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "General Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation:"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)
    paragraph7_text = "This is a non-residential course. However, you can apply for an accommodation " \
                      "vacancy at the Institute using Hostel Application Form. If successful, you will " \
                      "be required to pay Kshs.18,000 per term."
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees. Fees apply to each Academic Year which comprises of three" \
                                      "terms (including the term students will be on attachment). Fees is " \
                                      "payable as follows:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    paragraph8_text_list_item2_1_text = "Semester I: Kshs.59,950 (that includes registration fee " \
                                        "of Kshs.1,000) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Semester II: Kshs.58,950 payable at the beginning of Semester 2."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING " \
                                      "OR INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable. "
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item3_text = "HELB: Needy students may apply for HELB Loan. To apply, visit " \
                                      "HELB website on www.helb.co.ke or their Offices at Anniversary " \
                                      "Towers, Nairobi. Use the Serial Number (S.No.) on the first page " \
                                      "of this letter in place of Admission No. when applying for HELB Loan."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_certificate(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at the Kenya Institute of Mass Communication as a SELF – SPONSORED Student for " \
                      "a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Evenings and Weekends: - Monday – Friday " \
                      "(4.30 pm – 8.30pm) & Saturdays (8.00am – 4.00pm), at our Main Campus, Nairobi. " \
                      "It will take One (1) Academic Year."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "NB: Please note that upon successful completion of the certificate course, " \
                      "you will be eligible for re-admission into a two (2) year Upgrading Diploma " \
                      "but upon application."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "General Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation:"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)
    paragraph7_text = "This is a non-residential course. However, you can apply for an accommodation " \
                      "vacancy at the Institute using Hostel Application Form. If successful, you will " \
                      "be required to pay Kshs.18,000 per term."
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees. Fees apply to each Academic Year which comprises of three" \
                                      "terms (including the term students will be on attachment). Fees is " \
                                      "payable as follows:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.49,000 (that includes registration fee of " \
                                        "Kshs.1,000) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term II: Kshs.24,500 is payable at the beginning of Term 2."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term III: Kshs.24,500 is payable at the beginning of Term 3."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='          iii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING " \
                                      "OR INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable. "
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item3_text = "HELB: Needy students may apply for HELB Loan. To apply, visit " \
                                      "HELB website on www.helb.co.ke or their Offices at Anniversary " \
                                      "Towers, Nairobi. Use the Serial Number (S.No.) on the first page " \
                                      "of this letter in place of Admission No. when applying for HELB Loan."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_evening(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at the Kenya Institute of Mass Communication as a SELF – SPONSORED Student for " \
                      "a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Evenings and Weekends: - Monday – Friday " \
                      "(4.30 pm – 8.30pm) & Saturdays (8.00am – 4.00pm), at our Main Campus, " \
                      "Nairobi. It will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "NB: Please note that upon successful completion of the certificate course, " \
                      "you will be eligible for re-admission into a two (2) year Upgrading Diploma " \
                      "but upon application."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "General Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation:"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)
    paragraph7_text = "This is a non-residential course. However, you can apply for an accommodation " \
                      "vacancy at the Institute using Hostel Application Form. If successful, you will " \
                      "be required to pay Kshs.18,000 per term."
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees. Fees apply to each Academic Year which comprises of three" \
                                      "terms (including the term students will be on attachment). Fees is " \
                                      "payable as follows:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.51,500 (that includes registration fee of " \
                                        "Kshs.1,000) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term II: Kshs.25,250 payable at the beginning of Term 2."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term III: Kshs.25,250 payable at the beginning of Term 3."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='          iii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING " \
                                      "OR INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable. "
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item3_text = "HELB: Needy students may apply for HELB Loan. To apply, visit " \
                                      "HELB website on www.helb.co.ke or their Offices at Anniversary " \
                                      "Towers, Nairobi. Use the Serial Number (S.No.) on the first page " \
                                      "of this letter in place of Admission No. when applying for HELB Loan."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_upgrading(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at the Kenya Institute of Mass Communication as a SELF – SPONSORED Student for " \
                      "a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Evenings and Weekends: - Monday – Friday " \
                      "(4.30 pm – 8.30pm) & Saturdays (8.00am – 4.00pm), at our Main Campus, " \
                      "Nairobi. It will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "General Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation:"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)
    paragraph7_text = "This is a non-residential course. However, you can apply for an accommodation " \
                      "vacancy at the Institute using Hostel Application Form. If successful, you will " \
                      "be required to pay Kshs.18,000 per term."
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees. Fees apply to each Academic Year which comprises of three" \
                                      "terms (including the term students will be on attachment). Fees is " \
                                      "payable as follows:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.51,500 (that includes registration fee of " \
                                        "Kshs.1,000) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term II: Kshs.25,250 payable at the beginning of Term 2."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term III: Kshs.25,250 payable at the beginning of Term 3."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='          iii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING " \
                                      "OR INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable. "
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item3_text = "HELB: Needy students may apply for HELB Loan. To apply, visit " \
                                      "HELB website on www.helb.co.ke or their Offices at Anniversary " \
                                      "Towers, Nairobi. Use the Serial Number (S.No.) on the first page " \
                                      "of this letter in place of Admission No. when applying for HELB Loan."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_evening(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at the Kenya Institute of Mass Communication as a SELF – SPONSORED Student for " \
                      "a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered daily, during Evenings and Weekends: - Monday – Friday " \
                      "(4.30 pm – 8.30pm) & Saturdays (8.00am – 4.00pm), at our Main Campus, " \
                      "Nairobi. It will take Three (3) Academic Years."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, during working Hours, " \
                      "between 8.00am and 3.00pm.  Please ACCEPT or REJECT the offer by filling in the Acceptance " \
                      "Form, KIMC/KAB/ADM 002.  The DEADLINE for reporting will be Friday, 22nd September 2023."
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

    paragraph5_text = "NB: Please note that upon successful completion of the certificate course, " \
                      "you will be eligible for re-admission into a two (2) year Upgrading Diploma " \
                      "but upon application."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    paragraph5_text = "The Institute is located along Uholo Road, off Mombasa Road in Nairobi South ‘B’.  Use " \
                      "Matatu No. 11 or 12 that are boarded at the Bus Station, next to the former " \
                      "Kenya Bus Service stage"
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)
    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "General Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation:"
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)
    paragraph7_text = "This is a non-residential course. However, you can apply for an accommodation " \
                      "vacancy at the Institute using Hostel Application Form. If successful, you will " \
                      "be required to pay Kshs.18,000 per term."
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "Tuition Fees. Fees apply to each Academic Year which comprises of three" \
                                      "terms (including the term students will be on attachment). Fees is " \
                                      "payable as follows:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    paragraph8_text_list_item2_1_text = "Term I: Kshs.51,500 (that includes registration fee of " \
                                        "Kshs.1,000) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term II: Kshs.25,250 payable at the beginning of Term 2."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_1_text = "Term III: Kshs.25,250 payable at the beginning of Term 3."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='          iii)'))
    content.append(paragraph8_text_list_item2_1)

    paragraph8_text_list_item2_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING " \
                                      "OR INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable. "
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item3_text = "HELB: Needy students may apply for HELB Loan. To apply, visit " \
                                      "HELB website on www.helb.co.ke or their Offices at Anniversary " \
                                      "Towers, Nairobi. Use the Serial Number (S.No.) on the first page " \
                                      "of this letter in place of Admission No. when applying for HELB Loan."
    paragraph8_text_list_item3 = (Paragraph(paragraph8_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph8_text_list_item3)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response


def generate_pdf_eldoret(request, index_no):
    try:
        mystudent = Student.objects.get(index_number=index_no)
    except Student.DoesNotExist:

        return HttpResponse("Record not found", status=404)

    logo = "admission/static/images/logo.png"
    letterhead = "admission/static/images/letterhead.png"
    signature = "admission/static/images/sign.jpg"
    logo_img = Image(logo)
    letterhead_img = Image(letterhead)
    logo_img.hAlign = 'CENTER'
    letterhead_img.hAlign = 'CENTER'
    logo_img._width = 100
    letterhead_img._width = 480
    logo_img._height = 100
    letterhead_img._height = 48
    signature_img = Image(signature, width=220, height=100, hAlign='LEFT')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Calling_letter.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    table_styling = TableStyle([
        ('BACKGROUND', (0, 0), (5, 0), colors.gray),
        ('SPAN', (0, 4), (3, 4)),
        ('INNERGRID', (0, 0), (6, 6), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ])

    # Custom Styles --Start
    letter_style = ParagraphStyle(
        name='Letter',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        alignleft=10,
        fontSize=10,
        leading=8,
        leftIndent=354,
        spaceBefore=6,
        spaceAfter=2
    )

    letter2_style = ParagraphStyle(
        name='Letter2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=246,
        leading=8,
        spaceBefore=6,
        spaceAfter=2
    )

    letter3_style = ParagraphStyle(
        name='Letter3',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        spaceBefore=6,
        spaceAfter=8
    )

    blank_style = ParagraphStyle(
        name='Blank',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2
    )

    line_style = ParagraphStyle(
        name='Line',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=7,
        leading=8,
        spaceBefore=0,
        spaceAfter=0
    )

    number_style = ParagraphStyle(
        name='Number',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leftIndent=10,
        leading=-6,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent_style = ParagraphStyle(
        name='Normal_indent',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=30,
        spaceBefore=6,
        spaceAfter=6
    )

    normal_indent2_style = ParagraphStyle(
        name='Normal_indent2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=12,
        leftIndent=68,
        spaceBefore=6,
        spaceAfter=6
    )

    title2_style = ParagraphStyle(
        name='Title2',
        parent=styles['Normal'],
        fontName=_baseFontNameB,
        fontSize=10,
        leading=8,
        underline=5,
        spaceBefore=4,
        spaceAfter=8
    )

    content = [logo_img, letterhead_img]

    date_text = "2nd August 2023"
    date = Paragraph(date_text, letter_style)
    content.append(date)

    index = mystudent.index_number
    if len(index) == 10:
        index_text = ""
    else:
        index_text = "KCSE index Number: " + index
    indexno = Paragraph(index_text, letter2_style)
    content.append(indexno)

    serial_number = mystudent.serial_number
    serial_no_text = "S/No.: " + serial_number
    serial_no = Paragraph(serial_no_text, letter3_style)
    content.append(serial_no)

    full_name = mystudent.full_name
    full_name_text = full_name
    full_name = Paragraph(full_name_text, styles['Normal'])
    content.append(full_name)

    box_no = mystudent.box_no
    box_code = mystudent.box_code
    if box_code == "nan":
        box_no = "N/A"
        box_code = "N/A"
    post_text = "P.O. Box " + box_no + " - " + box_code
    post = Paragraph(post_text, styles['Normal'])

    content.append(post)

    town = mystudent.town
    if town == "nan":
        town = "N/A"
    post_code_text = town
    post_code = Paragraph(post_code_text, styles['Normal'])
    content.append(post_code)

    blank_text = " "
    blank = Paragraph(blank_text, blank_style)
    content.append(blank)

    num1 = mystudent.phone_number
    num2 = mystudent.phone_number2
    if num1 == "nan":
        num1 = "N/A"
        num2 = "N/A"
    mobile_text = "Mobile No: 0" + num1 + " / 0" + num2
    mobile = Paragraph(mobile_text, styles['Normal'])
    content.append(mobile)

    email = mystudent.email_address
    if email == "nan":
        email = "N/A"
    email_text = "Email: " + email
    email = Paragraph(email_text, styles['Normal'])
    content.append(email)

    line_text = "---------------------------------------------------------------------------------------------" \
                "--------------------------------------"
    line = Paragraph(line_text, styles['Normal'])
    content.append(line)

    title_text = "ADMISSION INTO THE KIMC 2023/2024 ACADEMIC YEAR (SEPTEMBER 2023 INTAKE)"
    title = Paragraph(title_text, title2_style)
    content.append(title)

    content.append(blank)

    paragraph1_text = "Following your application for admission into the Institute, I am pleased to offer you " \
                      "a place at Kenya Institute of Mass Communication (KIMC), as a Self – Sponsored Student " \
                      "for a Course leading to:"
    paragraph1 = Paragraph(paragraph1_text, styles['Normal'])
    content.append(paragraph1)

    line2_text = "_______________________________________________________________________________"
    line2 = Paragraph(line2_text, line_style)

    course = mystudent.course
    title2_text = course
    title2 = Paragraph(title2_text, title2_style)
    content.append(blank)
    content.append(title2)

    paragraph2_text = "The course will be offered in modules, at KIMC Eldoret Campus. It will be " \
                      "structured into eight (8) modules, three (3) projects and a three (3) months " \
                      "compulsory Industrial Attachment."
    paragraph2 = Paragraph(paragraph2_text, styles['Normal'])
    content.append(paragraph2)
    content.append(blank)

    paragraph3_text = "You are expected to report on Wednesday, 13th September 2023, between " \
                      "8.00am and 3.00pm. If you accept the offer, you will be expected to " \
                      "report for training punctually. Please ACCEPT or REJECT the offer by " \
                      "filling in the Acceptance Form, KIMC/KAB/ADM 002. Please note that " \
                      "failure to report for training by the deadline you will be assumed to " \
                      "have forfeited the chance. The DEADLINE for reporting will be on Friday, " \
                      "22nd September 2023."
    paragraph3 = Paragraph(paragraph3_text, styles['Normal'])
    content.append(paragraph3)
    content.append(blank)

    paragraph4_text = "However, this admission is subject to satisfactory verification of your " \
                      "academic documents by the KIMC authorities & KNEC. Please bring your " \
                      "ORIGINAL & COPIES of the K.C.S.E. Certificate/Results Slips, KCPE Certificate, " \
                      "School Leaving Certificate, National ID, & Birth Certificate, during " \
                      "registration. Download and fill the following admission packages (forms) " \
                      "that are available on our website: www.kimc.ac.ke, e-resources section. " \
                      "Please bring them during the reporting the day."
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

    paragraph5_text = "NB: Please note that upon successful completion of the module certificate course, " \
                      "you will be eligible for re-admission into a two (2) year Upgrading Diploma. " \
                      "However, you will need to apply."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    paragraph5_text = "You are expected to make your own travel arrangements. The Institute is " \
                      "located at Homecraft Centre, Pioneer Area, Eldoret Town."
    paragraph5 = Paragraph(paragraph5_text, styles['Normal'])
    content.append(blank)
    content.append(paragraph5)

    content.append(blank)
    content.append(blank)

    title3_text = "JOINING INSTRUCTIONS :"
    title3 = Paragraph(title3_text, title2_style)
    content.append(title3)

    no1_text = "1."
    paragraph6_text = "Requirements:"
    no1 = Paragraph(no1_text, number_style)
    paragraph6 = Paragraph(paragraph6_text, normal_indent_style)
    content.append(blank)
    content.append(no1)
    content.append(paragraph6)

    paragraph6_text_list_item1_text = "Stationery. All students MUST bring enough stationery (Writing Materials)."
    paragraph6_text_list_item1 = (Paragraph(paragraph6_text_list_item1_text, normal_indent_style,
                                            bulletText='               a)'))
    content.append(paragraph6_text_list_item1)

    paragraph6_text_list_item2_text = "Laptop. All KIMC Course are computer - aided. All students are encouraged to " \
                                      "buy a laptop. Please visit our website: www.kimc.ac.ke for recommended " \
                                      "specifications."
    paragraph6_text_list_item2 = (Paragraph(paragraph6_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph6_text_list_item2)

    no2_text = "2."
    paragraph7_text = "Accommodation. This is a NON-RESIDENTIAL course. However, there are private " \
                      "hostels that host students. Please make your personal arrangements."
    no2 = Paragraph(no2_text, number_style)
    paragraph7 = Paragraph(paragraph7_text, normal_indent_style)
    content.append(blank)
    content.append(no2)
    content.append(paragraph7)

    no3_text = "3."
    paragraph8_text = "Fees Structure (2023/2024): "
    no3 = Paragraph(no3_text, number_style)
    paragraph8 = Paragraph(paragraph8_text, normal_indent_style)
    content.append(no3)
    content.append(paragraph8)

    paragraph8_text_list_item1_text = "The Institute fees and charges are as below but are subject to review:"
    paragraph8_text_list_item1 = (Paragraph(paragraph8_text_list_item1_text, normal_indent_style,
                                            bulletText='            a)'))
    content.append(paragraph8_text_list_item1)
    content.append(blank)

    table_data = [
        ['No.', 'Fees', 'No. of Modules', 'Rate per Module Ksh.', 'Amount Payable (Ksh.)'],
        ['1', 'Administration and Registration', '-', '-', '1,000.00'],
        ['2', 'Tuition', '8', '15,000.00', '120,000.00'],
        ['3', 'STO Practical Session (Nairobi)', '-', '-', '4,500.00'],
        ['Total', '', '', '', '125,500.00'],
    ]
    table = Table(table_data)
    table.setStyle(table_styling)
    content.append(table)
    content.append(blank)

    paragraph8_text_list_item2_text = "Tuition Fees. Fees can be paid in full i.e., Ksh.125,500.00 or in " \
                                      "Three (3) instalments as follows:"
    paragraph8_text_list_item2 = (Paragraph(paragraph8_text_list_item2_text, normal_indent_style,
                                            bulletText='            b)'))
    content.append(paragraph8_text_list_item2)

    paragraph8_text_list_item2_1_text = "Term 1: Ksh.63,250.00 (that includes registration fee of " \
                                        "Ksh.1,000.00) payable during registration."
    paragraph8_text_list_item2_1 = (Paragraph(paragraph8_text_list_item2_1_text, normal_indent2_style,
                                              bulletText='            i)'))
    content.append(paragraph8_text_list_item2_1)
    content.append(blank)

    paragraph8_text_list_item2_2_text = "Term 2: Ksh.31,125.00, payable at the start of Term 2"
    paragraph8_text_list_item2_2 = (Paragraph(paragraph8_text_list_item2_2_text, normal_indent2_style,
                                              bulletText='           ii)'))
    content.append(paragraph8_text_list_item2_2)
    content.append(blank)

    paragraph8_text_list_item2_3_text = "Term 3: Ksh.31,125.00, payable at the start of Term 3"
    paragraph8_text_list_item2_3 = (Paragraph(paragraph8_text_list_item2_3_text, normal_indent2_style,
                                              bulletText='            iii)'))
    content.append(paragraph8_text_list_item2_3)
    content.append(blank)

    paragraph9_text_list_item3_text = "Mode of Payment: KIMC DOES NOT ACCEPT CASH PAYMENTS, AGENT BANKING OR " \
                                      "INSTITUTIONAL CHEQUES. All Payments MUST be paid to: Kenya Institute " \
                                      "of Mass Communication, Kenya Commercial Bank (KCB), KICC Branch, " \
                                      "Account No. 1143 244 362. Please note that fees once paid is NOT " \
                                      "refundable or transferable."
    paragraph9_text_list_item3 = (Paragraph(paragraph9_text_list_item3_text, normal_indent_style,
                                            bulletText='            c)'))
    content.append(paragraph9_text_list_item3)

    paragraph10_text_list_item4_text = "HELB: Needy students may apply for HELB Loan. To apply, visit HELB " \
                                       "website on www.helb.co.ke or their Offices at Anniversary Towers, " \
                                       "Nairobi. Use the Serial Number (S.No.) on the first page of this " \
                                       "letter in place of Admission No. when applying for HELB Loan."
    paragraph10_text_list_item4 = (Paragraph(paragraph10_text_list_item4_text, normal_indent_style,
                                             bulletText='            d)'))
    content.append(paragraph10_text_list_item4)
    content.append(blank)

    no4_text = "4."
    paragraph11_text = "Medical Cover: KIMC provides First Aid Medical Care Services ONLY. Parents/Guardians " \
                       "are FULLY responsible for ALL of their children’s medical expenses. Please note that " \
                       "all students MUST have an active medical insurance cover when reporting"
    no4 = Paragraph(no4_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no4)
    content.append(paragraph11)
    content.append(blank)

    no5_text = "5."
    paragraph12_text = "Discipline:  All students MUST at all times observe and abide by all KIMC Rules & " \
                       "Regulations as enshrined in the KIMC Academic Policy.  Carefully read & fill in " \
                       "the KIMC Form KIMC/KAB/ADM 005 available on our website. Please note that your " \
                       "studentship will depend on your academic performance and discipline, inside & outside " \
                       "the Institute."
    no5 = Paragraph(no5_text, number_style)
    paragraph10 = Paragraph(paragraph12_text, normal_indent_style)
    content.append(no5)
    content.append(paragraph10)
    content.append(blank)
    content.append(blank)

    no6_text = "6."
    paragraph11_text = "Correspondences: All correspondences MUST be addressed to the Director " \
                       "using the above addresses. "
    no6 = Paragraph(no6_text, number_style)
    paragraph11 = Paragraph(paragraph11_text, normal_indent_style)
    content.append(no6)
    content.append(paragraph11)
    content.append(blank)

    paragraph12_text = "May I take this opportunity to congratulate you on your admission and look forward to " \
                       "welcoming you at the Kenya Institute of Mass Communication. “CONGRATULATIONS”."
    paragraph12 = Paragraph(paragraph12_text, styles['Normal'])
    content.append(paragraph12)
    content.append(blank)
    content.append(blank)

    content.append(signature_img)

    doc.build(content)
    return response
