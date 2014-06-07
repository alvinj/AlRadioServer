#!/usr/bin/python

import ystockquote

print "\n\n___ STOCK QUOTES ___\n"

appl = ystockquote.get_price('AAPL')
print 'Apple: ' + appl + "\n"

att = ystockquote.get_price('T')
print 'AT&T: ' + att + "\n"

gtat = ystockquote.get_price('GTAT')
print 'GTAT: ' + gtat + "\n"

jcp = ystockquote.get_price('JCP')
print 'JCP: ' + jcp + "\n"

tsla = ystockquote.get_price('TSLA')
print 'TSLA: ' + tsla + "\n"



