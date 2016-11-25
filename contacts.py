# -*- coding: utf-8 -*-

import sqlite3
import csv
import re

con = sqlite3.connect('dbtest.db')
con.text_factory = str


def create_table():
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Address_book(id INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT, Surname TEXT, Address TEXT, email TEXT, Phone INTEGER);")


def add_contacts():
    name = raw_input("Enter first name: ")
    name = name.strip()

    lastname = raw_input("Enter surname: ")
    lastname = lastname.strip()

    adres = raw_input("Enter address: ")
    adres = adres.strip()

    correct = False
    while not correct:
        mail = raw_input("Enter e-mail: ")
        mail = mail.strip()
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", mail):
            print "### Wrong e-mail format. Try again. ###"
        else:
            correct = True

    cor = False
    while not cor:
        try:
            tel = int(raw_input("Enter phone number: "))
        except ValueError:
            print "### Not an integer. Try again. ###"
        else:
            cor = True


    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Address_book(FirstName, Surname, Address, email, Phone) VALUES(?, ?, ?, ?, ?)",
                    (name, lastname, adres, mail, tel))



def show_all_contacts():
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Address_book;")
        a = cur.fetchone()

        if a[0] > 0:
            cur.execute('SELECT * FROM Address_book;')
            while True:
                row = cur.fetchone()
                if not row:
                    break
                print str(row[0]), str(row[1]) + ";", row[2] + ";", row[3] + ";", row[4] + ";", str(row[5]) + "\n"
        else:
            print "### DB is empty ###"


def find_contact():
    find = raw_input("Search by first name/surname: ")
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Address_book WHERE UPPER(FirstName) LIKE ? OR UPPER(Surname) LIKE ? ; ',
                    ("%" + find + "%", "%" + find + "%"))
        all_rows = cur.fetchall()
        for row in all_rows:
            print "PK: " + str(row[0])
            print "First name: " + str(row[1])
            print "Surname: " + str(row[2])
            print "Address: " + str(row[3])
            print "E-mail: " + str(row[4])
            print "Phone number: " + str(row[5])


def delete_contact():
    with con:
        cur = con.cursor()
        delete_string = str(raw_input("Delete: "))
        cur.execute('DELETE FROM Address_book WHERE FirstName LIKE ? OR Surname LIKE ?; ',
                    ("%" + delete_string + "%", "%" + delete_string + "%"))
        if delete_string == "":
            return delete_contact()


def generate_csv():
    with con:
        cur = con.cursor()
        a = cur.execute('SELECT * FROM Address_book; ')

    with open("output_contacts.csv", "wb") as file2:
        s = csv.writer(file2, delimiter=";")
        s.writerow(['PK', 'FirstName', 'Surname', 'Address', 'E-mail', 'Phone'])
        for y in a:
            s.writerow(y)


def run_menu():
    print "\nPlease enter the number you wish to execute:\n\n" \
          "1. Add contact\n\n" \
          "2. Show contacts\n\n" \
          "3. Search\n\n" \
          "4. Delete contact\n\n" \
          "5. Export contacts to file\n\n" \
          "6. Exit\n"

    t = int(raw_input("Number: "))
    print "\n"

    if t == 1:
        add_contacts()
        return run_menu()

    elif t == 2:
        show_all_contacts()
        return run_menu()

    elif t == 3:
        find_contact()
        return run_menu()

    elif t == 4:
        delete_contact()
        return run_menu()

    elif t == 5:
        generate_csv()
        return run_menu()

    elif t == 6:
        print "Good bye!"
        if con:
            con.close()
        exit()


def main():
    create_table()
    print "Welcome to address book!"
    run_menu()


if __name__ == "__main__":
    main()
