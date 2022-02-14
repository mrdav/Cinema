import os
import MySQLdb
import random
import getpass
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
myrange = (1,  1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2 ,
        2.1,  2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3 ,  3.1,
        3.2,  3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4 ,  4.1,  4.2,
        4.3,  4.4,  4.5,  4.6,  4.7,  4.8,  4.9, 5)

try:
    db = MySQLdb.connect('localhost','user','pass','dbname',charset='utf8')
    pass
except:
    print("Could not establish a connection to the database. Please contact the staff")
    os.system('pause')
    quit()
cursor = db.cursor()

def menu():
    global choice
    print("1. View all movies")
    print("2. Book a Seat")
    print("3. Cancel a Reservation")
    print("4. Check your booking number")
    print("5. Rate a Movie")
    choice = str(input("Enter your choice: "))
    while choice not in ('1','2','3','4','5','6','7'):
        print("Invalid choice, options (1-6)")
        choice = input("Enter your choice: ")
    if choice == '1':
        print()
        view()
        print()
        menu()
    elif choice == '2':
        print()
        book()
        menu()
    elif choice == '3':
        print()
        cancel()
        menu()
    elif choice == '4':
        print()
        check()
        menu()
    elif choice == '5':
        print()
        vote()
        menu()
    elif choice == '6':
        usr = input("Enter username: ")
        if len(usr) == 0 or usr == '0':
            menu()
        pwd = getpass.getpass("Enter password: ")
        if len(pwd) == 0 or pwd == '0':
            menu()
        if usr != 'staff' or pwd != 'pass':
            print("Authentication failed.")
            menu()
        else:
            db.close()
            quit()
    elif choice == '7':
        staff()


        
def view():
    sel = cursor.execute("SELECT * FROM movies;")
    if sel == 0:
        print("No movies available")
    else:
        print("Everyday Screening")
        lst = cursor.fetchall()
        for row in lst:
            movname = row[0]
            first = row[1]
            sec = row[2]
            rate = row[3]
            votes = row[4]
            print("{}: {} , {}  Rate: {}/5 votes: {}\n".format(movname, first, sec, rate, votes))
def gen():
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','Z']
    numbers = ['1','2','3','4','5']
    randlet = random.choice(letters)
    randnum1 = random.choice(numbers)
    randnum2 = random.choice(numbers)
    return randlet + randnum1 + randnum2
def check():
    global bnum
    bnum = input("Enter your Booking Number: ")
    crs = cursor.execute("SELECT number FROM booked WHERE number = '{}';".format(bnum))
    while crs == 0:
        if bnum == '0' or bnum == 'back' or bnum == 'exit' or bnum == 'return' or bnum == ' ':
            menu()
        print("Could not identify {} please try again".format(bnum))
        bnum = input("Enter your Booking Number: ")
        crs = cursor.execute("SELECT number FROM booked WHERE number = '{}';".format(bnum))
    crs = cursor.execute("SELECT * FROM booked WHERE number = '{}';".format(bnum))
    ft = cursor.fetchall()
    print()
    print("Found an entry: {}  Movie Name: {}  Time: {}  Seat: {}  Name: {}".format(bnum, ft[0][1], ft[0][2], ft[0][3], ft[0][5]))
    print()
def book():
    print("Available movies:")
    print()
    crs = cursor.execute("SELECT movie FROM movies;")
    ft = cursor.fetchall()
    for i in ft:
        print(*i)
        print()
    newft = []
    for i in ft:
        newft.append(*i)
    mov = input("Choose a movie: ")
    while mov not in newft:
        if mov == '0' or mov == 'exit' or mov == '':
            menu()
        print("'{}' is not recognized. Please choose from the menu".format(mov))
        mov = input("Choose a movie: ")
    crs = cursor.execute("SELECT * FROM movies WHERE movie = '{}';".format(mov))
    ft = cursor.fetchall()
    ft = ft[0]
    print()
    print("{}".format(ft[1]))
    print("{}".format(ft[2]))
    print()
    tim = input("Choose Time: ")
    while tim not in (ft[1],ft[2]):
        if tim == '0' or tim == 'exit':
            menu()
        print("Error. Choose from the time above.")
        tim = input("Choose Time: ")
    name = input("Enter your Full Name: ")
    success = False
    while success == False:
        try:
            rcpt = input("Enter you email address: ")
            success = True
        except:
            print("A valid address is required")
            rcpt = input("Enter you email address: ")
    number = str(random.randint(10000, 99999))
    crs2 = cursor.execute("SELECT * FROM booked;")
    ft2 = cursor.fetchall()
    while number in ft2:
        number = str(random.randint(10000, 99999))
    seat = gen()
    while seat in ft2:
        seat = gen()
    cursor.execute("INSERT INTO booked (movie, name, number, seat, time, email) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(mov, name, number, seat, tim, rcpt))
    db.commit()
    print()
    print("Successfully booked a seat. Your unique Book Number: {}, Seat Number: {}. An email have been sent to you.".format(number, seat))
    try:
        fromaddr = "emailaddr"
        server = smtplib.SMTP('localhost', 587)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        server.starttls()
        msg['To'] = rcpt
        msg['Subject'] = "Your Booking Number for the movie {}".format(mov)
        body = "Hello {},\nYou have booked a seat for the movie {} and here is your information:\nBooking Number: {}\nSeat: {}\nMovie Starts at {}\nWhen you arrive, check the monitors for the room number\nHave Fun!\n\nThank you!".format(name, mov, number, seat, tim)
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.login(fromaddr, "pass")
        server.sendmail(fromaddr, rcpt, text)
        server.close
    except (ConnectionRefusedError,TimeoutError,smtplib.SMTPRecipientsRefused):
        print()
        print("Could not send email because the server is currently closed or the given address was invaild, however your seat has been successfully booked")
        print()
        menu()
    print()
def cancel():
    check()
    conf = input("Are you sure you want to delete the entry? Y/N: ")
    while conf not in ('Y','y','n','N','Yes','yes','No','no'):
        print("Not acceptable")
        conf = input("Are you sure you want to delete the entry? Y/N: ")
    if conf == 'y' or conf == 'Y' or conf == 'Yes' or conf == 'yes':
        print()
        print("Successfully canceled the reservation with booking number {}".format(bnum))
        print()
        cursor.execute("SELECT * FROM booked WHERE number = '{}';".format(bnum))
        ft = cursor.fetchall()
        rcpt = ft[0][4]
        try:
            fromaddr = "emailaddr"
            server = smtplib.SMTP('localhost', 587)
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            server.starttls()
            msg['To'] = rcpt
            msg['Subject'] = "Your seat for the movie {} has been Canceled".format(ft[0][1])
            body = "Hello {},\nYou recently have requested the cancellation of your seat for the movie {} and booking number {}. This email is a confirmation. If you did not cancel it, please reply to this email directly.\n\nHave a nice day!".format(ft[0][5], ft[0][1], bnum)
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server.login(fromaddr, "pass")
            server.sendmail(fromaddr, rcpt, text)
            server.close
        except (ConnectionRefusedError,TimeoutError,smtplib.SMTPRecipientsRefused):
            print()
            print("Could not send confirmation email because the server is currently closed or the recepient is invaild, however your booking number has been canceled")
            print()
        finally:
            cursor.execute("DELETE FROM booked WHERE number = '{}'".format(bnum))
            db.commit()
    else:
        print("User stopped the cancelation. Your Booking Number {} is still valid".format(bnum))
        print()
        menu()
def vote():
    lnum = input("Enter your last Booking Number: ")
    crs = cursor.execute("SELECT * FROM booked WHERE number = '{}';".format(lnum))
    ft2 = cursor.fetchall()
    if len(ft2) == 0:
        crs2 = cursor.execute("SELECT * FROM watched WHERE number = '{}';".format(lnum))
        ft = cursor.fetchall()
        if len(ft) == 0:
            print()
            print("You must watch the movie first in order to rate")
            print()
            menu()
    crs2 = cursor.execute("SELECT * FROM watched WHERE number = '{}';".format(lnum))
    ft = cursor.fetchall()
    if len(ft) == 0:
        print()
        print("Watch the movie '{}' first, and then come back to rate it!".format(ft2[0][1]))
        print()
        menu()
    elif lnum in ft[0]:
        movname = ft[0][1]
        rate = 0
        while rate not in myrange:
            try:
                rate = float(input("Enter Stars Rate for the movie '{}' (1-5): ".format(movname)))
                if rate in myrange:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Your rate is not being acceptable. Try again")
                rate = float(input("Enter Stars Rate for the movie '{}' (1-5): ".format(movname)))
        print()
        print("Your Rate has been submitted! {}/5 for the movie '{}'".format(rate, movname))
        print()
        cursor.execute("SELECT * FROM movies WHERE movie = '{}';".format(movname))
        ft = cursor.fetchall()
        totrate = ft[0][5] + rate
        votes = ft[0][4] + 1
        rate = totrate / votes
        cursor.execute("UPDATE movies SET totalrate = {:.1f}, votes = {}, rate = {:.1f} WHERE movie = '{}';".format(totrate, votes, rate, movname))
        cursor.execute("DELETE FROM watched WHERE number = '{}';".format(lnum))
        db.commit()
    else:
        print()
        print("Wrong Booking Number")
        print()
        menu()
def staff():
    usr = input("Enter username: ")
    pwd = getpass.getpass("Enter password: ")
    if usr != 'staff' or pwd != 'pass':
        print()
        print("Authentication Failed")
        print()
        menu()
    bnt = '1'
    while bnt != '0':
        bnt = str(input("Enter Booking Number: "))
        crs = cursor.execute("SELECT * FROM booked WHERE number = '{}';".format(bnt))
        ft = cursor.fetchall()
        if bnt == '0' or bnt == '':
            menu()
        while len(ft) == 0:
            if bnt == '0' or bnt == '':
                menu()
            print("Invaild Booking Number")
            bnt = input("Enter Booking Number: ")
            cursor.execute("SELECT * FROM booked WHERE number = '{}';".format(bnt))
            ft = cursor.fetchall()
        ft = ft[0]
        print("Found an entry: {}  Movie Name: {}  Time: {}  Seat: {}  Name: {}".format(bnt, ft[1], ft[2], ft[3], ft[5]))
        cnf = input("Confirm? y/n: ")
        while cnf not in ('y','n'):
            cnf = input("Confirm? y/n: ")
        if cnf == 'y':
            try:
                fromaddr = "emailaddr"
                server = smtplib.SMTP('localhost', 587)
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                server.starttls()
                rcpt = ft[4]
                msg['To'] = rcpt
                msg['Subject'] = "Did you like the movie {}? Rate now!".format(ft[1])
                body = "Hello {},\nYou recently watched the movie {}.\nPlease tell us and the world your impressions of the movie. Just bring your booking number together!\nThank you.\n\nHave a nice day!".format(ft[5], ft[1])
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                server.login(fromaddr, "pass")
                server.sendmail(fromaddr, rcpt, text)
                server.close()
            except (ConnectionRefusedError,TimeoutError,smtplib.SMTPRecipientsRefused):
                print()
                print("Could not send rate email, server closed or the recepient is invaild, however the operation was successful")
                print()
            finally:
                cursor.execute("INSERT INTO watched (email, movie, name, number) VALUES ('{}', '{}', '{}', '{}');".format(ft[4], ft[1], ft[5], bnt))
                cursor.execute("DELETE FROM booked WHERE number = '{}';".format(bnt))
                db.commit()
                print("Success")
        elif cnf == 'n':
            cnf2 = input("Not confirmed. Also delete the entry? y/n: ")
            while cnf2 not in ('y','n'):
                cnf2 = input("Not confirmed. Also delete the entry? y/n: ")
            if cnf2 == 'y':
                cursor.execute("DELETE FROM booked WHERE number = '{}';".format(bnt))
                db.commit()
                print("Success")
            elif cnf2 == 'n':
                print("Not deleted. Booking number is still valid.") 
menu()
