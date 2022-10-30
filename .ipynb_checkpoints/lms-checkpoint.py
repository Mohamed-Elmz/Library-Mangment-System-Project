"""
PSU Library Insight Software, Mohamed Elmanzalawi, Compsci 131 final project
Colaborators: Dylan Swedberg
"""

import numpy as np

def get_option():
    """
    Display menu options
    """
    
    print("PSU Library Insight Software\n\nAvalible Services:\n")
    print(" 1) Check Avalability\n 2) Most popular books\n 3) Borrow ratio\n 4) Usage ratio\n 5) Pending Fines\n 6) Exit") 
    option = int(input("Please enter desired service: "))
    
    if option in [1,2,3,4,5,6]:
        return option
    else:
        print("Invalid option!")
        return get_option()
    
def load_book_list(file_name):
    """
    Read book list file
    """
    book_id = []
    names = []
    copies = []
    restricted = []
    
    copies_left = []
    total_borrowed_days = []
    total_available_days = []
    largest_no_copies_borrowed = []
    
    
    booklist = open(file_name, "r")
    
    
    line = booklist.readline()
    i = 0
    while line != "":
        line = line.rstrip("\n")
        m = line.split("#")
    
        names.append (m[0])
        copies.append (int(m[1]))
        restricted.append (m[2])
        book_id.append(i)
        i += 1 
        copies_left.append(int(m[1]))
        total_borrowed_days.append(0)
        total_available_days.append(0)
        largest_no_copies_borrowed.append(0)
        
        
        line = booklist.readline()
        
       
        
    print(len(names), " books loaded!")
    
    #        0         1      2         3           4             5                      6                     7
    return [book_id, names, copies, restricted, copies_left, total_borrowed_days, total_available_days, largest_no_copies_borrowed]

"""
def get_index_max_number(a):
    indx = 0
    max_value = 0
    for i in range(len(a)):
        if a[i] > max_value:
            max_value = a[i]
            indx = i
    return indx, max_value
"""

def get_book_id(book_name, books):
    """
    Get book record for a given book name
    """
    i = 0 
    for bk in books[1]:  # for each book name
        if bk == book_name:       
            return books[0][i]
        i = i+1
    print(book_name, " not found")
    return -1

def get_borrow_ratio(books):
    br = []
    
    for i in range(len(books[0])):
        br.append(round((100 * books[5][i])/(200*books[2][i]),0))     #TODO: read total days from the log
    return br

#TODO remove this wrong version
def get_borrow_ratio2(books):
    br = []
    
    for i in range(len(books[0])):
        br.append(round((100 * books[5][i]*books[7][i])/(200*books[2][i]),0))     #TODO: read total days from the log
    return br

def get_borrow_ratio3(books):
    br = []
    
    for i in range(len(books[0])):
        # print(books[1][i], books[5][i], books[6][i])  # for testing
        br.append(round((100*books[5][i])/(books[6][i]),0))     # total_borrowed_days/total_available_days
    return br



"""
def sort_books_by_borrow_ratio(br, names):
    ind = np.argsort(br)
    ordered_names = [names[i] for i in ind]
    return ordered_names
"""

def load_library_logs(logs_file, book_list_file, books, stop_day=10000):
    """
    Read library log file
    """
    borrow_day = []
    borrow_sn = []
    borrow_bn = []
    borrow_dbf = []   # no of days the books is borrowed for
    borrow_due_day = []
    borrow_restricted = []
    
    return_day = []
    return_sn = []
    return_bn = []
    return_charged = []
    
    add_day = []
    add_bn = []
    
    pay_day = []
    pay_sn = []
    pay_amount = []
    
    
    charge_day = [] 
    charge_sn = []
    charge_amount = []
    
    
    
    i = 1
    reader = open(logs_file, "r")
    
    
    line = reader.readline()

    while line != "":
        
        line = line.rstrip("\n")
        m = line.split("#")

        if m[0] == "B":
            if int(m[1])>stop_day:
                break
            # read borrow log
            borrow_day.append(int(m[1]))
            borrow_sn.append(m[2])
            borrow_bn.append(m[3])
            borrow_dbf.append(int(m[4]))
            borrow_due_day.append(int(m[1]) + int(m[4])) # if you borrow on day 1 for three days, the due date is 4
            bkid = get_book_id(m[3], books)
            borrow_restricted.append(books[3][bkid]) 
            
            # update book profile
            books[4][bkid] = books[4][bkid] - 1  # decrement no of copies left
            # Note: our expectation is that the logs are all valid but this test showed that this not the case for the following entries
            """
            Copies left can't be negative  B#53#Jennifer#Intro to python#1
            Copies left can't be negative  B#64#Adam#Intro to python#4
            Copies left can't be negative  B#67#Greg#Intro to python#4
            Copies left can't be negative  B#78#Greg#Intro to python#3
            Copies left can't be negative  B#83#Greg#Intro to python#3
            Copies left can't be negative  B#85#Jennifer#Intro to python#5
            Copies left can't be negative  B#95#Kartik#Intro to c#1
            Copies left can't be negative  B#101#Alyssa#Intro to c#1
            Copies left can't be negative  B#109#Alyssa#Intro to c#6
            Copies left can't be negative  B#125#Alyssa#Intro to c#5
            Copies left can't be negative  B#134#Alyssa#Intro to c#6
            Copies left can't be negative  B#139#Kartik#Intro to c#1
            Copies left can't be negative  B#150#Amanda#Intro to c#4
            Copies left can't be negative  B#167#Jerome#Intro to c#1
            Copies left can't be negative  B#180#Kartik#Intro to c#1
            Copies left can't be negative  B#182#Alyssa#Intro to c#2
            Copies left can't be negative  B#197#Alyssa#Intro to c#4
            """
            if books[4][bkid] < 0:
                print("Copies left can't be negative ", line)
            
            books[5][bkid] = books[5][bkid] + int(m[4])
            current_no_copies_borrowed = books[2][bkid] - books[4][bkid]
            if current_no_copies_borrowed > books[7][bkid]:
                books[7][bkid] = current_no_copies_borrowed

        elif m[0] == "R":
            if int(m[1])>stop_day:
                break
                
            bkid = get_book_id(m[3], books)

            return_day.append(m[1])
            charge_day.append(m[1])
            return_sn.append(m[2])
            charge_sn.append(m[2])
            return_bn.append(m[3])
            dd, rst = get_borrow_record(m[2], m[3], borrow_day, borrow_sn, borrow_bn, borrow_due_day, borrow_restricted)
            #print("Due day for ", line, ": ", dd)   # for testing
            diff = int(m[1]) - int(dd)
            #print("Book retruned and difference is", diff)  # for testing
            if diff <= 0:
                books[5][bkid] += diff
                return_charged.append("0") #TODO turen into number
                charge_amount.append("0")
            else:
                books[5][bkid] += diff
                if rst == "TRUE":
                    return_charged.append(str(diff*5))
                    charge_amount.append(str(diff*5))
                else:
                    return_charged.append(str(diff))
                    charge_amount.append(str(diff))
            
            # update book profile
            
            books[4][bkid] += 1
                    

        elif m[0] == "A":
            if int(m[1])>stop_day:
                break

            # Does the book exist
            bkid = get_book_id(m[2], books)
            if bkid != - 1:
                books[2][bkid] += 1
            else:   # add a new book
                bkid = len(books[0])
                books[0].append(bkid)
                books[1].append(m[2])
                books[2].append(1)
                books[3].append("FALSE")  # Note: add command sould specify whether the new books is restricted or not
                books[4].append(1)
                books[5].append(0)
                books[6].append(0)
                books[7].append(0)
                
 
        elif m[0] == "P":
            if int(m[1])>stop_day:
                break

            pay_day.append(m[1])
            pay_sn.append(m[2])
            pay_amount.append(m[3])

        else:  # end of logs 
            if len(m) > 1:
                print("log file error in line ", i)
            else:
                total_log_days = int(m[0])    # e.g., 200 days
            
        i = i+1
        line = reader.readline()
    print("Total logs read ", i)    
    borrow_logs = [borrow_day, borrow_sn, borrow_bn, borrow_due_day, borrow_restricted]
    return_logs = [return_day, return_sn, return_bn, return_charged]
    add_logs = [add_day, add_bn]
    pay_logs = [pay_day, pay_sn, pay_amount]
    charge_logs = [charge_day, charge_sn, charge_amount]
    
    
    if stop_day==10000:
        
        # Update the total_avilable_days for each book
        # 1. available days for initial copies. Get the initital no of copies from the booklist

        init_books = load_book_list(book_list_file)
        for i in range(len(init_books[0])): # for each book id
            copies = init_books[2][i]
            books[6][i] += (copies*total_log_days)

        # avialble days for added books
        i = 1
        reader = open(logs_file, "r")
        line = reader.readline()

        while line != "":

            line = line.rstrip("\n")
            m = line.split("#")

            if m[0] == "A":
                if int(m[1])>stop_day:
                    break
                bkid = get_book_id(m[2], books)
                books[6][bkid] += (total_log_days - int(m[1]))

            i = i+1
            line = reader.readline()
            
        # Update total_borrowed_days at the end of the log for pending returns
        for i in range(len(borrow_logs[3])):
            diff = borrow_logs[3][i] - total_log_days
            if diff > 0:
                # check that the student did not return the book early before its due
                query = borrow_logs[1][i]+borrow_logs[2][i]
                bd = borrow_logs[0][i]
                book_returned = False
                for j in range(len(return_logs[0])):
                    if int(return_logs[0][j]) >= bd:
                        rquery = return_logs[1][j]+return_logs[2][j]
                        if query == rquery:
                            book_returned = True
                if book_returned == False:        
                    bkid = get_book_id(borrow_logs[2][i], books)
                    books[5][bkid] -= diff
                
    
    return [borrow_logs, return_logs, add_logs, pay_logs, charge_logs], books


def get_borrow_record(student_name, book_name, borrow_day, borrow_sn, borrow_bn, borrow_due_day, borrow_restricted):
    """
    Get the most recent borrow log for a given student and book
    """
    
    query = student_name + book_name   # unique assuming the student can't borrow two copies of the same book
    
    index = -1
    for i in range(len(borrow_sn)):
        if query == (borrow_sn[i] + borrow_bn[i]):
            index = i
    if index == -1:
        print("Error ", student_nabme, " never borrowed ", book_name)
    
    return  borrow_due_day[index], borrow_restricted[index]
            
        
    
    
    
def get_num_borrowed_books(std_name, logs):
    """
    Determine how many books are borrowed by a given student
    """
    borrow_records = logs[0]
    num_borrowed_books = 0
    for name in borrow_records[1]:
        if name == std_name:
            num_borrowed_books = num_borrowed_books + 1
        
    returned_records = logs[1]
    num_returned_books = 0
    for name in returned_records[1]:
        if name == std_name:
            num_returned_books = num_returned_books + 1
            
    return num_borrowed_books - num_returned_books
 
def get_owned_charges(std_name, logs):

    returned_records = logs[1]
    
    
    names = returned_records[1]
    charges = returned_records[3]
    
    total_charges = 0
    for i in range(len(names)):
        if std_name == names[i]:
            total_charges = total_charges + float(charges[i])
            
   
    
    payment_records = logs[3]
    names = payment_records[1]
    amounts = payment_records[2]
    
    total_payments = 0
    for i in range(len(names)):
        if std_name == names[i]:
            total_payments = total_payments + float(amounts[i])
            
    return total_charges - total_payments
    

def can_borrow(on_day, std_name, book_name, num_days, books_file, logs_file):
    sub_books = load_book_list(books_file)
    sub_logs, sub_books = load_library_logs(logs_file, books_file, sub_books, on_day)
    
    bkid = get_book_id(book_name, sub_books)
    n = sub_books[1][bkid]
    c = sub_books[4][bkid]
    r = sub_books[3][bkid]
    
    print(on_day, n, c)
    
    if c ==  0:
        print("Book not available")
        return False
    if r == "TRUE" and num_days > 7:
        print("Restricted books can't be borrowed for more than 7 days")
        return False
    if  num_days > 28:
        print("Book can't be borrowed for more than 28 days")
        return False
    
    if get_num_borrowed_books(std_name, sub_logs) >= 3:
        print("Student can't borrow more than 3 books")
        return False
    
    #  check for pending fines
    if get_owned_charges(std_name,sub_logs) > 0:
        print("Student has unpaid fines")
        return False
        
    return True
    

def get_pending_fines(day, pay_logs, charge_logs):
    # get list of all charged students until the given day
    charged_students = []
    for i in range(len(charge_logs[0])):
        if int(charge_logs[0][i]) <= day:
            sn = charge_logs[1][i]
            if sn in charged_students:
                pass  # do nothing
            else:
                charged_students.append(charge_logs[1][i])
        else:
            break
            
    pending_fines_report = []
    pfr_sn = []
    pfr_total_charge = []
    pfr_total_payment = []
    pfr_pending_fine = []
    
    for i in range(len(charged_students)):
        sn = charged_students[i]
        total_charge_i = 0
        for j in range(len(charge_logs[0])):
            if sn == charge_logs[1][j]:
                total_charge_i += float(charge_logs[2][j])
        
        total_pay_i = 0
        for j in range(len(pay_logs[0])):
            if sn == pay_logs[1][j]:
                total_pay_i += float(pay_logs[2][j])
                
        pfr_sn.append(sn)
        pfr_total_charge.append(total_charge_i)
        pfr_total_payment.append(total_pay_i)
        pfr_pending_fine.append(total_charge_i - total_pay_i)
        
    
    pending_fines_report = [pfr_sn, pfr_total_charge, pfr_total_payment, pfr_pending_fine]
    return pending_fines_report


            
#####  Main Code #############
book_list_file = "./booklist-2.txt"
logs_file = "./librarylog-3.txt"

# Read data
books = load_book_list(book_list_file)
logs, books = load_library_logs(logs_file, book_list_file, books)


cont = True
while cont:
    opt = get_option()
    if opt == 1:
        book_str = input("Enter <on_day>#<student_name>#<book_name>#<days>")
        a = book_str.split("#")
        if can_borrow(int(a[0]),a[1],a[2], int(a[3]), book_list_file, logs_file):
            print("Yes")
        else:
            print("No")
        
    elif opt == 2:
        
        indx_total_borrowed_days_sorted = np.flip(np.argsort(books[5]))
        for indx in indx_total_borrowed_days_sorted:
            print( books[1][indx], " was borrowed for ", books[5][indx])
    elif opt == 3:
        br = get_borrow_ratio3(books)
        indx_br_sorted = np.flip(np.argsort(br))
        i = 0
        print("Top three books with the highest borrow ratio are:")
        for indx in indx_br_sorted:
            print( books[1][indx], " had borrow ratio of ", br[indx])
            i += 1
            if i > 2:
                break
        
    elif opt == 4:
        br = get_borrow_ratio3(books)
        indx_br_sorted = np.flip(np.argsort(br))
        for indx in indx_br_sorted:
            print( books[1][indx], " had borrow ratio of ", br[indx])
        
    elif opt == 5:
        day = int(input("Enter a day: "))
        pending_fines = get_pending_fines(day, logs[3], logs[4])
        # Now, we need to sort the records by the pending fines
        sorted_indx = np.flip(np.argsort(pending_fines[3]))
        for indx in sorted_indx:
            print(pending_fines[0][indx], pending_fines[3][indx])
        
    if opt == 6:
        cont = False
