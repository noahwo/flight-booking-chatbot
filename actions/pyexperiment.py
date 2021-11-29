import sqlite3
from datetime import datetime, timedelta
from pprint import pprint

def main():
    # print_flights()
    # get_all_dep()
    # init_db_customer()
    
    order_flight()
    # date0=""
    # id="7853265374"
    
    # """find out the code bought by user FROM TABLE customer"""
    # conn = sqlite3.connect('rasa1.db')
    # cs=conn.cursor()
    # cs.execute("SELECT bought_flight FROM customer where idnum='"+id+"'")
    # rs=cs.fetchall()
    # rc=cs.rowcount
    # cs.close()
    # conn.close()
    
    # for r in rs:
    #     for i in r:
            
    #         code=i
    # print("bought_flight: "+code)
    # # """set bought_flight as null firstly, then validate"""
    # # conn = sqlite3.connect('rasa1.db')
    # # cs=conn.cursor()
    # # cs.execute("update customer set bought_flight='' where idnum='"+id+"'")
    # # cs.close()
    # # conn.commit() 
    # # conn.close()
    
    # if code=="":
    #     msg="Sorry, you don't have the order, or the ID you provided was incorrect."
    # else:
        
    #     """get date and price from flight table"""
    #     conn = sqlite3.connect('rasa1.db')
    #     cs=conn.cursor()
    #     # FIXME the line blow has issue 
    #     cs.execute("SELECT date FROM flight where code='"+code+"'") 
    #     rsD=cs.fetchall() 
    #     cs.close() 
    #     conn.close() 
        
    #     conn = sqlite3.connect('rasa1.db')  
    #     cs=conn.cursor() 
    #     cs.execute("SELECT price FROM flight where code='"+code+"'") 
    #     rsP=cs.fetchall() 
    #     cs.close()
    #     conn.close()
        
    #     for r in rsD:
    #         for i in r:
    #             date0=i
    #     for r in rsP:
    #         for i in r:
    #             price=i
                
    #     print("price: "+str(date0))   
    #     print("date: "+str(price))    
         
    #     today1 = datetime.today().date()  
    #     print(today1) 
    #     print(date0)
    #     date=datetime.strptime(date0,"%Y-%m-%d").date()
    #     time_interval_day=(date-today1).days
    #     time_interval_hour=(date-today1).days*24
    #     if time_interval_day >=48:
    #         msg="You seccessfully canceled the order of {} {} days before. You will get full refund of {}".format(code,time_interval_day,price)
    #     else:
    #         price2=str(int(price)*0.8).split('.')[0]
    #         msg="You seccessfully canceled the order of {}, but only {} hours days before. You will get 80%\ of the refund {}, which is RMB {}.".format(code,time_interval_hour,price,price2)
            
    #     print(msg)    
        
        
        
        
        
def dateC():
    date_str="2021-11-26"
    today = datetime.date.today()    
    
    date=datetime.datetime.strptime(date_str,"%Y-%m-%d").date()
    
    day=(date-today).days*24
    print(str(day)+" hours")
    # formatted_date1 = time.strptime(first_date, "%d/%m/%Y")
    
    
    
def order_flight():
    
    conn = sqlite3.connect('rasa1.db')

    cs=conn.cursor()
    id="7853265374"

    code="AA234"
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    
    cs.execute("update customer set bought_flight='{}' where idnum='{}'".format(code,id))
    rc=cs.rowcount
    
    cs.close()
    conn.commit()
    conn.close()
    
    print("Executed to order flight: update customer set bought_flight='{}' where idnum={}".format(code,id))
    
    if rc ==0:
        msg="Sorry, no account found. You may register first."
    else:
        msg="You seccessfully ordered the ticket. Please check the information again:\nCODE:\t{}".format(code)
    print(msg)

def cancel_order():
    id="zsl222222"
    conn = sqlite3.connect('rasa1.db')

    cs=conn.cursor()
    code=""
    cs.execute("SELECT code FROM flight where id='"+id+"'")
    rs=cs.fetchall()
    for r in rs:
        print(r)
        code=r
    cs.execute("update customer set bought_flight='' where idnum='"+id+"'")
    cs.close()
    conn.commit() 
    conn.close()
    rc=cs.rowcount
    
    if rc ==0:
        msg="Sorry, you don't have the order, or your ID was incorrect."
    else:
        msg="You seccessfully canceled the order of {}.".format(code)
        
def test_register():
    id="27e4748333"
    fullname="Wu Guanghan"
    email="1570048612@qq.com"
    email2=email
    # email=email.split('@')[0]+"'||'&'||'"+email.split('@')[1]
    fullname=fullname.split(' ')[0]+"-"+fullname.split(' ')[1]
    
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute("insert into customer(fullname, idnum, email) values('"+fullname+"','"+id+"','"+email+"')")
    print("insert into customer(fullname, idnum, email) values('"+fullname+"','"+id+"','"+email+"')")
    cs.close()
    conn.close()
    
    msg=""
    rc=cs.rowcount
    print(rc)
    if rc > 0:
        fullname=fullname.split('-')[0]+" "+fullname.split('-')[1]
        msg="You seccessfully registered. Please check the information again: \nFullname: \n\t{}\nID:\n\t{}\nEmail: \n\t{}".format(fullname,id,email2)
    # DONE TODO: Finish this method
    else:
        msg="Failed to gegister, please contact our staff by saying \"I want staffservice\"."
    
    print(msg)


def init_db_customer():
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('''drop table customer;''') 
    cs.execute('''create table customer( id integer primary key autoincrement, fullname varchar(30) not null, idnum varchar(30) not null, email varchar(30) not null, bought_flight varchar(30));''')
    
    cs.close()
    conn.commit()
    conn.close()
    
def init_db():
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('''drop table flight;''')
    cs.execute('''drop table customer;''') 
    
    cs.execute('''create table flight(id integer primary key autoincrement, dep varchar(20) not null, des varchar(20) not null, code varchar(8) not null,  date varchar(10) not null,  price int(8) not null);''')
    
    cs.execute('''create table customer( id integer primary key autoincrement, fullname varchar(30) not null, idnum varchar(15) not null, email varchar(30) not null, bought_flight varchar(30));''')
    
    cs.close()
    conn.commit()
    conn.close()

def insert_flights():
    sql_file=open('insert_flight.sql')
    sql_str=sql_file.read()   
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.executescript(sql_str)
    cs.close()
    conn.commit()
    conn.close()    
    
    
"""insert new customer"""
def insert_customer(list):   
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute("insert into customer(idnum, fullname, email,username) values('"+list[0]+"','"+list[1]+"','"+list[2]+"','"+list[3]+"')")
    cs.close()
    conn.commit()
    conn.close()    
    
"""make order"""
def make_order(id,flightCode):   
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute("UPDATE customer SET bought_flight="+flightCode+" WHERE idnum='"+id+"'")
    cs.close()
    conn.commit()
    conn.close()   
    
def cancel_order():
    id="zsl222222"
        
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    code=""
    cs.execute("SELECT bought_flight FROM customer where idnum='"+id+"'")
    print("SELECT bought_flight FROM customer where idnum="+id+"")
    rs=cs.fetchall()
    for r in rs:
        for i in r:
            print(i)
            code=i
    cs.execute("update customer set bought_flight='' where idnum='"+id+"'")
    cs.close()
    conn.commit() 
    conn.close()
    rc=cs.rowcount
    
    if rc ==0:
        msg="Sorry, you don't have the order, or your ID was incorrect."
    else:
        msg="You seccessfully canceled the order of {}.".format(code)

    print(msg)
def print_flights():
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('select * from flight')
    rs=cs.fetchall()
    # pprint(rs)
    list="\n###################################################\n# Currently, we provide the flights listed below: #\n###################################################\n"

    for i in rs:
        s=str(i).split('\'')
        s[8]=s[8].split(' ')[1].split(')')[0]
        strr="{0[1]} -> {0[3]},\t{0[5]},\t{0[7]}, ￥{0[8]}\n".format(s)
        list=list+strr
    cs.close()
    conn.close() 
    print(list)
    
def print_customer():
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('select * from customer')
    rs=cs.fetchall()
    if rs is None:
        pprint("The table is empty.")
    else:
        for r in rs:
            pprint(r)
            
    cs.close()
    conn.close()   
    
"""select flight on conditions"""
# querry=["Helsinki","Nanjing","2019-08-24"]
# querry2=["Helsinki","Nanjing"]
def query_flight(list):
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    pprint(list)
    if len(list) ==3:
        cs.execute("SELECT * FROM flight where dep= '"+list[0]+ "' AND des= '"+list[1]+"' AND date='"+list[2]+"'")
    elif len(list) ==2:
        cs.execute("SELECT * FROM flight where dep= '"+list[0]+ "' AND des= '"+list[1]+"'")
       
    rs=cs.fetchall()
    
    if len(rs) <= 0:
        print("The table is empty.")
    else:
        for r in rs:
            pprint(r)
    cs.close()
    conn.close()  

def get_all_dep():
    
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('select des from flight')
    rs=cs.fetchall()
    
    dep_list=[]
    for r in rs:
        r=str(r).split('\'')[1]
        if r not in dep_list:
            dep_list.append(r)
            
    print(dep_list)

def get_all_date():
    
    conn = sqlite3.connect('rasa1.db')
    cs=conn.cursor()
    cs.execute('select date from flight')
    rs=cs.fetchall()
    
    date_list=[]
    for r in rs:
        r=str(r).split('\'')[1]
        if r not in date_list:
            date_list.append(r)
            
    print(date_list)
    
    
if __name__=='__main__':
    main()