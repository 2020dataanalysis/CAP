import smtplib
s = smtplib.SMTP()
s.connect( 'email-smtp.us-west-1.amazonaws.com', 587 )
s.starttls()
s.login( 'AKIAW57DST4XSROYTFG5', 'BLBxhlQCOyI8ULqg90Zy0NDnMZXrIAN80Qw6BYfZlHqt' )
msg = 'Hello from Python !'
s.sendmail( '2018supersam@gmail.com', '2018supersam@gmail', msg )

https://stackoverflow.com/questions/51768041/python3-smtp-valueerror-server-hostname-cannot-be-an-empty-string-or-start-with

smtp = smtplib.SMTP('smtp.gmail.com')
smtp.connect('smtp.gmail.com','587')


import smtplib
s = smtplib.SMTP('smtp.gmail.com')
s.connect( 'smtp.gmail.com', 587 )
s.starttls()
s.login( 'AKIAW57DST4XSROYTFG5', 'BLBxhlQCOyI8ULqg90Zy0NDnMZXrIAN80Qw6BYfZlHqt' )
msg = 'Hello from Python !'
s.sendmail( '2018supersam@gmail.com', '2018supersam@gmail', msg )
