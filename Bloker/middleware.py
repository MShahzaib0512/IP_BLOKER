from .models import *
from django.http import HttpResponseForbidden,HttpResponse
import geoip2
from ip_bloker import settings
import logging
from django.contrib.gis.geoip2 import GeoIP2

class IpMiddleWare:
 def __init__(self, get_response):
  self.get_response=get_response
  
 def __call__(self,request):
  user_ip=request.META.get('REMOTE_ADDR')
  forwarded_user_ip=request.META.get('HTTP_X_FORWARDED_FOR')
  print(user_ip)
  print(forwarded_user_ip)
  ip=forwarded_user_ip.split(',')[0].strip() if forwarded_user_ip else user_ip
  print(ip)
  if IP_BLOCK.objects.filter(name=ip):
   return HttpResponseForbidden("Access Denied(Ip blocked)")

  return self.get_response(request)
 
 
class Country_ip_Middleware:
  
  def __init__(self,get_response):
   self.get_response=get_response
   self.geoip=GeoIP2(settings.GEOIP_PATH)
   
  def __call__(self,request):
   user_ip=request.META.get('REMOTE_ADDR')
   forwarded_user_ip=request.META.get('HTTP_X_FORWARDED_FOR')

   ip=forwarded_user_ip.split(',')[0].strip() if forwarded_user_ip else user_ip
   
   try:
    country=self.geoip.country(ip)["country_code"]
    if country in settings.BLOCKED_COUNTRIES:
     return HttpResponseForbidden('Access denied')
   except:
    logging.error("Failed to find ip")
    
   return self.get_response(request)