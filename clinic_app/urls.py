from django.urls import path
from . import views

urlpatterns = [


    path('login', views.login),
    path('add-person', views.register_patient),
    path('data-person',views.dataView_Status),

    path('search-person/',views.search_report_date),
    path('create-person',views.create_save_data),
    path('show-person',views.dataView_Status_view),
    path('show-person1',views.dataView_Status_view_1),

    path('show-person/<int:pk>',views.CusDetail),
    path('product',views.ProListView),
    
    path('add-status',views.update_123),


    path('product/<int:pk>',views.ProDetail),
    path('product-edit',views.ProEdit),
    path('product-delete/<int:pk>',views.Prodel),

    path('shop-type',views.dataView_Status_view_Product),
    path('search-product/',views.search_report_product),

    path('create-order',views.create_order),
    path('get-order',views.get_orders),
    path('get-pay',views.get_pays),

    path('pay',views.change_order_status),
    path('report-order',views.get_orders_2),
    path('search-status/', views.search_report_date_3),
    path('choose/',views.send_data),
    path('choose-product/',views.send_data_user),
    path('send-doctor',views.change_order_status_1),
    path('change-status',views.change_status),
    path('report-order-1',views.get_order_reports_1)

    
]
from django.conf import settings  
from django.conf.urls.static import static  
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  