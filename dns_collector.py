# -*- coding: utf-8 -*-

import os
import time
import socket
import dns.resolver
import threading
from urlparse import urlparse
import fileinput
import subprocess
import pytz
from datetime import datetime

# set dns
main_dns = '8.8.8.8'
sub_dns = '8.8.4.4'

def nslookup(DOMAIN):
      resolver = dns.resolver.Resolver()
      try:
            # main dns query
            resolver.nameservers = [main_dns]
            answers = resolver.query(DOMAIN)
            time.sleep(1)
      except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            # sub dns query
            resolver.nameservers = [sub_dns]
            answers = resolver.query(DOMAIN)
            time.sleep(1)
      
      for rdata in answers:
            return (resolver.nameservers[0], rdata.address)

def getDomain(PATH,FNAME):
      with open(PATH + '' + FNAME, 'r') as f:
            maldomain = f.readlines()

      if len(maldomain)>0:
            for i in range(0,len(maldomain)):
                  fmt = '%Y-%m-%d %H:%M:%S'
                  seoul = pytz.timezone('Asia/Seoul')
                  local_time = seoul.localize(datetime.now())

                  if maldomain[i][:4]!="http":
                        maldomain[i]="http://" + maldomain[i].rstrip()
                  
                  (dns, ip) = nslookup(urlparse(maldomain[i]).hostname)
                  maldomain[i] = "%s,%s,%s" % ("http" + maldomain[i][4:], str(ip), str(dns))

                  maldomain[i] = local_time.strftime(fmt) + "," + maldomain[i]
      else:
            maldomain = "No URL in File"
      
      return maldomain

def main():
      # Output file
      result = open('result.csv', 'a')
      try:
            output = subprocess.check_output(['tail', '-n 1', 'result.csv'], universal_newlines=True)
            count = int(output.split(',')[0])
      except:
            count = 0
      
      for item in getDomain("./","list.txt"):
            count += 1
            result.write(str(count) + "," + item + "\n")
      result.close()

if __name__ == '__main__':
      print "main dns: %s" % main_dns
      print "sub dns: %s" % sub_dns 
      while True:
            t = threading.Thread(target=main)
            t.start()
            t.join()
            time.sleep(3600)
