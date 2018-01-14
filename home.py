# -*- coding: utf-8 -*-

import os
import time
import socket
import dns.resolver
import threading
from urlparse import urlparse

# set dns
main_dns = '8.8.8.8'
sub_dns = '4.4.4.4'

def nslookup(DOMAIN):
   t = threading.Timer(3600, nslookup, args=[DOMAIN])
   t.start()
   resolver = dns.resolver.Resolver()
   try:
      resolver.nameservers = [main_dns]
      answers = resolver.query(DOMAIN)
   except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
      resolver.nameservers = [sub_dns]
      answers = resolver.query(DOMAIN)
   
   for rdata in answers:
      return (resolver.nameservers[0], rdata.address)

def getDomain(PATH,FNAME):
   with open(PATH + '' + FNAME, 'r') as f:
      maldomain = f.readlines()

   if len(maldomain)>0:
      for i in range(0,len(maldomain)):
         #print i

         now = time.localtime()
         s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

         if maldomain[i][:4]!="http":
            maldomain[i]="http://" + maldomain[i].rstrip()
       
         (dns, ip) = nslookup(urlparse(maldomain[i]).hostname)
         maldomain[i] = "%s,%s,%s" % ("http" + maldomain[i][4:], str(ip), str(dns))

         maldomain[i] = str(i) + "," +  s + "," + maldomain[i]

         print maldomain[i]

   else:
      maldomain = "No URL in File"

   return maldomain

def main():
   result = open('result.csv', 'a')

   for item in getDomain("./","list.txt"):
      result.write("%s\n" % item)

if __name__ == '__main__':
   main()


# http://n3015m.tistory.com/341
