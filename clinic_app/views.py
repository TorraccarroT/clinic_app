from .models import *
from rest_framework import viewsets
# from .api_module import *
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication 

from rest_framework.permissions import IsAuthenticated, IsAdminUser , AllowAny
# Create your views here.
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        
        if user.is_status == 0:
            btn_login = '0'
            check = '0'
        elif user.is_status == 1:
            btn_login = '1'
            check = '1'
        elif user.is_status == 2:
            btn_login = '2'
            check = '2'
        else:
            return Response({'error': 'ไม่พบข้อมูล'}, status=400)

        
        response_data = {
            'accessToken': token.key,
            'status': 'ok',
            'btn-login': btn_login,
            'check': check,
            'id': user.id,
            'username': user.username,

        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie('username', user.username)
        response.set_cookie('user_id', user.id)
        
        return response
    else:
        return Response({'error': 'เกิดข้อผิดพลาด'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def your_view(request):
    # โค้ดส่วนที่เกี่ยวข้องกับการบันทึกข้อมูลใหม่ลงในฐานข้อมูล
    serializer = Auction_Topic_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def get_previous_number(request):
    last_data = Data.objects.order_by('-id').first()  # หาข้อมูลล่าสุดจากฐานข้อมูล

    if last_data:
        previous_number = last_data.previous_number
    else:
        previous_number = None

    return Response({'previous_number': previous_number})



from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
import pytz
from datetime import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
def register_patient(request):
    current_year = (datetime.now().year + 543) % 100
    last_data = Data.objects.order_by('-id').first()

    if last_data:
        last_number = last_data.number
        last_year = int(last_number[2:6])

        if last_year < current_year:
            new_number = 1
        else:
            if last_number and last_number[6:].isdigit():
                last_number_int = int(last_number[6:])
            else:
                last_number_int = 0
            new_number = last_number_int + 1

        new_clinic_number = f'CN{str(current_year).zfill(2)}{str(new_number).zfill(4)}'

        while Data.objects.filter(number=new_clinic_number).exists():
            new_number += 1
            new_clinic_number = f'CN{str(current_year).zfill(2)}{str(new_number).zfill(4)}'
    else:
        new_clinic_number = f'CN{str(current_year).zfill(2)}0001'

    new_data = Data.objects.create(
        number=new_clinic_number,
        firstname=request.data.get('firstname'),
        lastname=request.data.get('lastname'),
        tel=request.data.get('tel'),
        id_person=request.data.get('id_person'),
        address_current=request.data.get('address_current'),
        tel_emergency=request.data.get('tel_emergency'),
        sickdisease=request.data.get('sickdisease'),
        sex=request.data.get('sex'),
        date=datetime.strptime(request.data.get('date'), '%Y-%m-%d').date(),
        drug_allergy=request.data.get('drug_allergy'),
        career=request.data.get('career'),
        name_company=request.data.get('name_company'),
        note=request.data.get('note'),
        image_sick = request.FILES.get('image_sick')

    )

    # ทำสิ่งที่คุณต้องการกับ new_data ที่ได้
    serializer = Auction_Topic_Serializer(new_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def dataView_Status(request):
    try:        
        if request.method == 'GET':
            snippets =  Data.objects.all().order_by('-id')
            # filter(sick_status=0)
            serializer = Auction_Topic_Serializer(snippets,  many=True)
            return Response(serializer.data)
    
        else:
            data = {'message': 'เกิดข้อผิดพลาด'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as data:
        data = {'message': 'เกิดข้อผิดพลาด'}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def dataView_Status_view(request):
    try:        
        if request.method == 'GET':
            snippets = Data.objects.filter(Q(sick_status=1) | Q(sick_status=2) | Q(sick_status=3)).order_by('-id')
            serializer = Auction_Topic_Serializer(snippets, many=True)
            return Response(serializer.data)
        else:
            data = {'message': 'เกิดข้อผิดพลาด'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        data = {'message': 'เกิดข้อผิดพลาด'}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([AllowAny])
def dataView_Status_view_1(request):
    Show_Report = request.query_params.get('Show_Report')
    if Show_Report:
        orders = Save_Data.objects.values(
                'person_data__number',
                'person_data__firstname',
                'person_data__lastname',
                'person_data__tel',
                'person_data__sex',
                'person_data__date',
                'person_data__drug_allergy',
                'person_data__id_person',
                'person_data__career',
                'person_data__address_current',
                'person_data__name_company',
                'person_data__tel_emergency',
                'person_data__note',
                'person_data__sickdisease',
                'person_data__image_sick',
                'person_data__sick_status',
                'type_sick_data',
                'sick_data'

            ).filter(person_data__id=Show_Report)



    if not orders:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)
    
    order_data = []
    for order in orders:
        data = {
            'person_data__number': order['person_data__number'],
            'person_data__firstname': order['person_data__firstname'],
            'person_data__lastname': order['person_data__lastname'],
            'person_data__tel': order['person_data__tel'],
            'person_data__sex': order['person_data__sex'],
            'person_data__date': order['person_data__date'].strftime('%d/%m/%Y'),
            'person_data__drug_allergy': order['person_data__drug_allergy'],
            'person_data__id_person': order['person_data__id_person'],
            'person_data__career': order['person_data__career'],
            'person_data__address_current': order['person_data__address_current'],
            'person_data__name_company': order['person_data__name_company'],
            'person_data__tel_emergency': order['person_data__tel_emergency'],
            'person_data__note': order['person_data__note'],
            'person_data__sickdisease': order['person_data__sickdisease'],
            'person_data__image_sick': order['person_data__image_sick'],
            'person_data__sick_status': order['person_data__sick_status'],
            'type_sick_data': order['type_sick_data'],
            'sick_data': order['sick_data']



        }
        order_data.append(data)

    return Response(order_data)

from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def search_report_date(request):
    search = request.GET.get('search')

    if search:
        reports = Data.objects.filter(
            Q(number__icontains=search) |
            Q(firstname__icontains=search) |
            Q(lastname__icontains=search) |
            Q(tel__icontains=search)
        ).order_by('-id')
    else:
        reports = Data.objects.order_by('-id')

    if not reports:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    report_data = [
        {
            'number': report.number,
            'firstname': report.firstname,
            'lastname': report.lastname,
            'tel': report.tel,
            'sex': report.sex or "ไม่ระบุ",
            'date': report.date,
            'drug_allergy': report.drug_allergy,
            'id_person': report.id_person,
            'career': report.career,
            'address_current': report.address_current,
            'name_company': report.name_company,
            'tel_emergency': report.tel_emergency,
            'note': report.note,
            'sickdisease': report.sickdisease,
            'image_sick': report.image_sick.url if report.image_sick else None,
            'sick_status': report.sick_status,
        }
        for report in reports
    ]

    return Response(report_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_save_data(request):
    # รับข้อมูลจาก request
    data_id = request.data.get('data_id')
    type_sick_data = request.data.get('type_sick_data')
    sick_data = request.data.get('sick_data')
    if not (data_id and type_sick_data and sick_data):
            return Response({'message': 'ไม่พบข้อมูล'}, status=400)
    # try:
    #     # ตรวจสอบว่าข้อมูลซ้ำหรือไม่
    #     Save_Data.objects.get(person_data_id=data_id, type_sick_data=type_sick_data, sick_data=sick_data)
    #     return Response({'message': 'ข้อมูลซ้ำกัน'}, status=400)
    # except ObjectDoesNotExist:
    #     pass

    try:
        # สร้าง Save_Data
        save_data = Save_Data.objects.create(person_data_id=data_id, type_sick_data=type_sick_data, sick_data=sick_data)

        # อัปเดต sick_status เป็น 1 ใน Data
        data = Data.objects.get(id=data_id)
        data.sick_status = 1
        data.save()

        return Response({'message': 'สร้าง Save_Data เรียบร้อยแล้ว'}, status=201)
    except Data.DoesNotExist:
        return Response({'message': 'ไม่พบข้อมูล Data'}, status=404)



@api_view(['GET'])
@permission_classes([AllowAny])
def CusDetail(request, pk):
    try:
        snippet = Data.objects.get(pk=pk)
    except Data.DoesNotExist:
        data = {'message': 'หาข้อมูลไม่เจอ'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Auction_Topic_Serializer(snippet)
        
        return Response(serializer.data)
    
from datetime import datetime

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_123(request):
    show_Id = request.data.get('show_Id')
    sick_status = request.data.get('sick_status')
    sick_date = request.data.get('sick_date')  # เปลี่ยน request.date เป็น request.data
    if not (sick_status and show_Id ):
            return Response({'message': 'ไม่กรอกพาราม'}, status=400)
    try:
        product = Data.objects.get(pk=show_Id)
        product.sick_status = sick_status
        product.date = sick_date
        product.save()
        serializer = Auction_Topic_Serializer_Status(product)
        response_data = {
                'status': 'สำเร็จ',
                'message': 'ส่งสถานะสำเร็จ',
                'data': serializer.data
            }
        return Response(response_data, status=200)
 

    
    except Data.DoesNotExist:
        return Response({"error": "เกิดข้อผิดพลาด"}, status=404)

    


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def ProListView(request):
    try:
        if request.method == 'GET':
            snippets = Shop_Product.objects.get_queryset()
            serializer = Product_Serializer(snippets, many=True)
            data = list(serializer.data)
            return Response(data)
        elif request.method == 'POST':
            serializer = Product_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {'message': 'เกิดข้อผิดพลาด'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        data = {'message': 'เกิดข้อผิดพลาด'}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def ProDetail(request, pk):
    try:
        snippet = Shop_Product.objects.get(pk=pk)
    except Shop_Product.DoesNotExist:
        data = {'message': 'หาข้อมูลไม่เจอ'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Product_Serializer(snippet)
        
        return Response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([AllowAny])
def ProEdit(request):
    id = request.data.get('id')
    shop_code = request.data.get('shop_code')
    shop_name = request.data.get('shop_name')
    shop_qty = request.data.get('shop_qty')
    shop_ps = request.data.get('shop_ps')
    shop_type = request.data.get('shop_type')
    shop_count = request.data.get('shop_count')
    shop_price = request.data.get('shop_price')

    if not (shop_code and id and shop_name and shop_qty and shop_ps and shop_type and shop_count and shop_price):
        return Response({'message': 'ไม่พบข้อมูล'}, status=400)

    try:
        product = Shop_Product.objects.get(pk=id)
        product.shop_code = shop_code
        product.shop_name = shop_name
        product.shop_qty = shop_qty
        product.shop_ps = shop_ps
        product.shop_type = shop_type
        product.shop_count = shop_count
        product.shop_price = shop_price

        product.save()
        serializer = Product_Serializer(product)
        response_data = {
            'status': 'สำเร็จ',
            'message': 'แก้ไขสำเร็จ',
            'data': serializer.data
        }
        return Response(response_data, status=200)
    
    except Shop_Product.DoesNotExist:
        return Response({"error": "ไม่พบข้อมูล"}, status=404)

    
@api_view(['DELETE'])
@permission_classes([AllowAny])
def Prodel(request, pk):
    try:
        product =  Shop_Product.objects.get(pk=pk)      
    except Shop_Product.DoesNotExist:
        data = {'message': 'เกิดข้อผิดพลาด'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    data = {'message': 'ลบข้อมูลแล้ว'}
    return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def dataView_Status_view_Product(request):
    try:        
        if request.method == 'GET':
            snippets = Shop_Product.objects.filter(shop_type = 'ความงาม')
            # filter(sick_status=0)
            serializer = Product_Serializer(snippets,  many=True)
            return Response(serializer.data)
    
        else:
            data = {'message': 'เกิดข้อผิดพลาด'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as data:
        data = {'message': 'เกิดข้อผิดพลาด'}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def generate_receipt_number(current_year, new_number):
    return f'TEST{str(current_year).zfill(2)}{str(new_number).zfill(4)}'  
from django.db.models import Max
import datetime

from datetime import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    data = request.data

    # สร้าง Order
    order_number = generate_order_number()
    order = Order.objects.create(
        number=order_number,
        patient_id=data['patient'],
        credit_card=data['credit_card'],
        address=data['address'],
        input_1=data['input_1'],
        input_2=data['input_2'],
        input_3=data['input_3'],
        doctor_1=data['doctor_1']
    )

    # สร้าง OrderItem
    for item_data in data['items']:
        product = Shop_Product.objects.get(id=item_data['product'])
        price = product.shop_price
        qty = item_data['qty']
        sum_price = price * qty

        if product.shop_qty < qty:
            return Response({'message': 'สินค้าหมด'}, status=400)

        # ตัด stock
        product.shop_qty -= qty
        product.save()

        OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            qty=qty,
            sum_price=sum_price
        )

    return Response({'message': 'สร้างสำเร็จ'},status=status.HTTP_201_CREATED)


def generate_order_number():
    now = datetime.now()
    current_year = (now.year + 543) % 100

    # ค้นหาจำนวนคำสั่งซื้อในปีปัจจุบัน
    current_year_orders = Order.objects.filter(number__startswith=f'TEST{current_year}')
    order_count = current_year_orders.count()

    new_sequence = order_count + 1

    order_number = f"TEST{current_year}{new_sequence:04d}"
    return order_number


@api_view(['GET'])
@permission_classes([AllowAny])
def search_report_product(request):
    search = request.GET.get('search')

    if search:
        reports = Shop_Product.objects.filter(
            Q(shop_code__icontains=search) |
            Q(shop_name__icontains=search) |
            Q(shop_qty__icontains=search) |
            Q(shop_ps__icontains=search) |
            Q(shop_type__icontains=search) |
            Q(shop_qty__icontains=search) |
            Q(shop_count__icontains=search)  |
            Q(shop_price__icontains=search)  

        ).filter(shop_type='ความงาม').order_by('-id')
    else:
        reports = Shop_Product.objects.filter(shop_type='ความงาม').order_by('-id')

    if not reports:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    report_data = [
        {
            'shop_code': report.shop_code,
            'shop_name': report.shop_name,
            'shop_qty': report.shop_qty,
            'shop_ps': report.shop_ps,
            'shop_type': report.shop_type,
            'shop_count': report.shop_count,
            'shop_price': report.shop_price,
        }
        for report in reports
    ]

    return Response(report_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_orders(request):
    Show_Report = request.data.get('Show_Report')
    if not Show_Report:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)
    print(Show_Report)
    print(type(Show_Report))
    orders = OrderItem.objects.values(
         'order__number',
         'order__patient',
         'order__created_at',
         'order__credit_card',
         'order__pay_check',
         'order__address',
         'product__shop_code',
         'product__shop_name',
         'product__shop_qty',
         'product__shop_ps',
         'product__shop_type',
         'product__shop_count',
         'product__shop_price',
         'sum_price',


       
        ).filter(order__number=Show_Report)

    if not orders:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)
    order_data = []
    for order in orders:
        data = {

            'ORDER ID': order['order__number'],
            'User': order['order__patient'],
            'Create_Date': order['order__created_at'],
            'Credit_Card': order['order__credit_card'],
            'Payment': order['order__pay_check'],
            'Address': order['order__address'],
            'Product_Code': order['product__shop_code'],
            'Product_Qty': order['product__shop_qty'],
            'Product_Ps': order['product__shop_ps'],
            'Product_Type': order['product__shop_type'],
            'Product_Count': order['product__shop_count'],
            'Product_Price': order['product__shop_price'],
            'Product_Sum Price': order['sum_price'],
      

        }

        order_data.append(data)

    # order_data = order_data.pop()
    return Response(order_data)





@api_view(['GET'])
@permission_classes([AllowAny])
def get_pays(request):
    try:
        order_items = OrderItem.objects.values(
            'order__number',
            'order__patient__id',
            'order__patient__firstname',
            'order__patient__lastname',
            'order__patient__number',
            'order__patient__tel_emergency',
            'order__patient__tel',
            'order__pay_status',
            'order__pay_check',
            'qty',
            'price',
            'product__shop_name',
            'sum_price'
        ).order_by('-id')

        if not order_items:
            return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)

        order_data = []
        prev_order_number = None
        order_items_data = []

        for order_item in order_items:
            order_number = order_item['order__number']

            if order_number != prev_order_number:
                if prev_order_number:
                    order_data.append({
                        'ORDER_ID': prev_order_number,
                        'User_ID': prev_order['order__patient__id'],
                        'First_Name': prev_order['order__patient__firstname'],
                        'Last_Name': prev_order['order__patient__lastname'],
                        'Clinic_Num': prev_order['order__patient__number'],
                        'Tel_EMG': prev_order['order__patient__tel_emergency'],
                        'Tel': prev_order['order__patient__tel'],
                        'Pay_Date': prev_order['order__pay_check'].strftime('%d-%m-%Y'),
                        'Status': prev_order['order__pay_status'],
                        'Items': order_items_data
                    })

                prev_order_number = order_number
                order_items_data = []

            item_data = {
                'Product': order_item['product__shop_name'],
                'Quantity': order_item['qty'],
                'Price': order_item['price'],
                'Total_Price': order_item['sum_price'],
            }
            order_items_data.append(item_data)
            prev_order = order_item

        if prev_order:
            order_data.append({
                'ORDER_ID': prev_order_number,
                'User_ID': prev_order['order__patient__id'],
                'First_Name': prev_order['order__patient__firstname'],
                'Last_Name': prev_order['order__patient__lastname'],
                'Clinic_Num': prev_order['order__patient__number'],
                'Tel_EMG': prev_order['order__patient__tel_emergency'],
                'Tel': prev_order['order__patient__tel'],
                'Pay_Date': prev_order['order__pay_check'].strftime('%d-%m-%Y'),
                'Status': prev_order['order__pay_status'],
                'Items': order_items_data
            })

        return Response(order_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def change_order_status(request):
    order_id = request.data.get('order_id')  # รับ order_id จาก request.data
    new_status = request.data.get('new_status')  # รับสถานะใหม่จาก request.data
    if not order_id and new_status :
            return Response({'message': 'ไม่สามารถดำเนินการได้'}, status=status.HTTP_400_BAD_REQUEST)
    try:
   
        order_item = Order.objects.get(number=order_id)
        order_item.pay_status = new_status
        order_item.save()
        return Response({'message': 'เปลี่ยนสถานะเรียบร้อยแล้ว'})
    except OrderItem.DoesNotExist:
        return Response({'message': 'ไม่พบ OrderItem ที่ระบุ'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_orders_1(request):

    Show_Report = request.data.get('Show_Report')
    print(Show_Report)
    print(type(Show_Report))

    # ตรวจสอบว่าไม่มีข้อมูลหรือ Show_Report เป็นค่าว่าง
    if not Show_Report:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_items = OrderItem.objects.filter(order__number=Show_Report)
    except OrderItem.DoesNotExist:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)

    if not order_items:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)

    order_data = []
    for order_item in order_items:
        order = order_item.order
        data = {
            'User': f"{order.patient.firstname} {order.patient.lastname}",
            'Address': order.address,
            'Num': order.number,
            'Create_At': order.created_at,
            'Credit_Card': order.credit_card,
            'Payment': order.pay_check,
            'Item': order_item.product.shop_name,
            'Item_Count': order_item.product.shop_count,
            'Item_Qty': order_item.qty,
            'Item_Price': order_item.product.shop_price,
            'Item_SumPrice': order_item.sum_price,
        }
        order_data.append(data)

    return Response(order_data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_orders_2(request):
    Show_Report = request.query_params.get('Show_Report')
    if not Show_Report:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Show_Report:
        orders = OrderItem.objects.values(
            'order__number',
            'order__patient__firstname',
            'order__patient__lastname',
            'order__patient__address_current',
            'order__created_at',
            'order__credit_card',
            'order__pay_check',
            'product__shop_name',
            'product__shop_qty',
            'product__shop_ps',
            'product__shop_type',
            'product__shop_count',
            'product__shop_price',
            'sum_price',
            'order__doctor_1',
            'qty',
        ).filter(order__number=Show_Report)
    else:
        orders = OrderItem.objects.values(
            'order__number',
            'order__patient__firstname',
            'order__patient__lastname',
            'order__patient__address_current',
            'order__created_at',
            'order__credit_card',
            'order__pay_check',
            'product__shop_name',
            'product__shop_qty',
            'product__shop_ps',
            'product__shop_type',
            'product__shop_count',
            'product__shop_price',
            'sum_price',
            'order__doctor_1'
        )

    if not orders:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_404_NOT_FOUND)
    
    order_data = []
    for order in orders:
        data = {
            'FirstName': order['order__patient__firstname'],
            'LastName': order['order__patient__lastname'],
            'Address': order['order__patient__address_current'],
            'Num': order['order__number'],
            'Create_At': order['order__created_at'].strftime('%d/%m/%Y'),
            'Credit_Card': order['order__credit_card'],
            'Payment': order['order__pay_check'].strftime('%d/%m/%Y'),
            'Item': order['product__shop_name'],
            'Item_Count': order['product__shop_count'],
            'Item_Qty': order['qty'],
            'Item_Price': order['product__shop_price'],
            'Item_SumPrice': order['sum_price'],
                            'doctor_doc':order['order__doctor_1']


        }
        order_data.append(data)

        # ตรวจสอบว่าข้อมูลซ้ำหรือไม่
        existing_report = OrderReport.objects.filter(
            first_name=order['order__patient__firstname'],
            last_name=order['order__patient__lastname'],
            address=order['order__patient__address_current'],
            order_number=order['order__number'],
            created_at=order['order__created_at'],
            credit_card=order['order__credit_card'],
            payment_date=order['order__pay_check'],
            item_name=order['product__shop_name'],
            item_count=order['product__shop_count'],
            item_quantity=order['qty'],
            item_price=order['product__shop_price'],
            item_total_price=order['sum_price'],
            user_doctor=order['order__doctor_1']

        ).exists()

        if not existing_report:
            OrderReport.objects.create(
                first_name=order['order__patient__firstname'],
                last_name=order['order__patient__lastname'],
                address=order['order__patient__address_current'],
                order_number=order['order__number'],
                created_at=order['order__created_at'],
                credit_card=order['order__credit_card'],
                payment_date=order['order__pay_check'],
                item_name=order['product__shop_name'],
                item_count=order['product__shop_count'],
                item_quantity=order['qty'],
                item_price=order['product__shop_price'],
                item_total_price=order['sum_price'],
                user_doctor=order['order__doctor_1']
            )
        else:
            data['Message'] = 'ข้อมูลซ้ำ'

    return Response(order_data, status=status.HTTP_200_OK)

from rest_framework.request import Request
@api_view(['GET'])
@permission_classes([AllowAny])
def get_order_reports_1(request):
    Show_Report = request.query_params.get('Show_Report')
    if not Show_Report:
        return Response({'message': 'ไม่พบข้อมูล'}, status=status.HTTP_400_BAD_REQUEST)
    order_reports = OrderReport.objects.filter(order_number=Show_Report)
    serializer = Auction_Topic_Serializer_Data_1(order_reports, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from datetime import date

@api_view(['GET'])
@permission_classes([AllowAny])
def search_report_date_3(request):
    sick_num = request.GET.get('sick_num')

    if sick_num == '1' or sick_num == '2' or sick_num =='3' or sick_num == '1,2,3':
        sick_status_filters = sick_num.split(',')
        reports = Data.objects.filter(sick_status__in=sick_status_filters).order_by('-id')
    elif sick_num == '4' or sick_num == '5' or sick_num == '4,5':
        if sick_num == '4':
            sick_status_filters = ['2'] 
        if sick_num == '5':
            sick_status_filters = ['3','4'] 
        if sick_num == '4,5':
            sick_status_filters = ['2','3','4']
        reports = Data.objects.filter(sick_status__in=sick_status_filters,date=date.today()).order_by('-id')
    else:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    if not reports:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    report_data = [
        {
            'id':report.id,
            'number': report.number,
            'firstname': report.firstname,
            'lastname': report.lastname,
            'tel': report.tel,
            'sex': report.sex or "ไม่ระบุ",
            'date': report.date,
            'drug_allergy': report.drug_allergy,
            'id_person': report.id_person,
            'career': report.career,
            'address_current': report.address_current,
            'name_company': report.name_company,
            'tel_emergency': report.tel_emergency,
            'note': report.note,
            'sickdisease': report.sickdisease,
            'image_sick': report.image_sick.url if report.image_sick else None,
            'sick_status': report.sick_status,
        }
        for report in reports
    ]

    return Response(report_data)





@api_view(['GET'])
@permission_classes([AllowAny])
def send_data(request):
    search = request.GET.get('search')


    if search:
        reports = Shop_Product.objects.filter(
           
            Q(shop_type__icontains=search) |
            Q(shop_name__icontains=search) 

    

        ).filter(
    Q(shop_type='ใช้ในการรักษา') |
    Q(shop_type='ยา') |
    Q(shop_type='ทั้งหมด')| Q(shop_type='ความงาม')
).order_by('-id')
    else:
        reports = Shop_Product.objects.filter(Q(shop_type='ใช้ในการรักษา') | Q(shop_type='ยา') | Q(shop_type='ทั้งหมด') | Q(shop_type='ความงาม')).order_by('-id')

    if not reports:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    report_data = [
        {
            'id': report.id,
            'shop_code': report.shop_code,
            'shop_name': report.shop_name,
            'shop_qty': report.shop_qty,
            'shop_ps': report.shop_ps,
            'shop_type': report.shop_type,
            'shop_count': report.shop_count,
            'shop_price': report.shop_price,
        }
        for report in reports
    ]

    return Response(report_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def send_data_user(request):
    search = request.GET.get('search')


    if search:
        reports = Shop_Product.objects.filter(
           
            Q(id__icontains=search) 
    

        ).order_by('-id')
    else:
        return Response({'msg':'ไม่พบข้อมูล'})

    if not reports:
        return Response({'message': 'ไม่พบข้อมูล'}, status=404)

    report_data = [
        {
            'id': report.id,
            'shop_code': report.shop_code,
            'shop_name': report.shop_name,
            'shop_qty': report.shop_qty,
            'shop_ps': report.shop_ps,
            'shop_type': report.shop_type,
            'shop_count': report.shop_count,
            'shop_price': report.shop_price,
        }
        for report in reports
    ]
    report_data = report_data.pop()

    return Response(report_data)




@api_view(['POST'])
@permission_classes([AllowAny])
def change_order_status_1(request):
    
    order_id = request.data.get('order_id')
    insert_1 = request.data.get('insert_1')
    insert_2 = request.data.get('insert_2')
    insert_3 = request.data.get('insert_3')

    if not order_id or not insert_1 or not insert_2 or not insert_3:
        return Response({'message': 'ไม่สามารถดำเนินการได้'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_item = Order.objects.get(number=order_id)
        order_item.input_1 = insert_1
        order_item.input_2 = insert_2
        order_item.input_3 = insert_3

        order_item.save()
        return Response({'message': 'เปลี่ยนสถานะเรียบร้อยแล้ว'})
    except Order.DoesNotExist:
        return Response({'message': 'ไม่พบ Order ที่ระบุ'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['PUT'])
@permission_classes([AllowAny])
def change_status(request):
    user_id = request.data.get('user_id')  # รับ order_id จาก request.data
    new_status = request.data.get('new_status')  # รับสถานะใหม่จาก request.data
    if not user_id and new_status :
            return Response({'message': 'ไม่สามารถดำเนินการได้'}, status=status.HTTP_400_BAD_REQUEST)
    try:
   
        order_item = Data.objects.get(id=user_id)
        order_item.sick_status = new_status
        order_item.save()
        return Response({'message': 'เปลี่ยนสถานะเรียบร้อยแล้ว'})
    except OrderItem.DoesNotExist:
        return Response({'message': 'ไม่พบ ID ที่ระบุ'}, status=status.HTTP_404_NOT_FOUND)