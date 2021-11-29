# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"
import yagmail
import sqlite3
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import FormValidation, SlotSet


class ValidateFlightForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_flight_form"
    
    def validate_departure(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute('select dep from flight')
        rs=cs.fetchall()
        
        dep_list=[]
        dep_str=""
        for r in rs:
            r=str(r).split('\'')[1]
            if r not in dep_list:
                dep_list.append(r)
                
        for d in dep_list:
            dep_str=dep_str+d+", "
        slot_value=slot_value.title()    
        if slot_value not in dep_list:
            dispatcher.utter_message(text="I didn't find any flight departs from {}, we currently provide flights departs from {}".format(slot_value, dep_str))
            return {"departure": None}
        dispatcher.utter_message(text=f"Ok, your departure is {slot_value}")
        return {"departure": slot_value}

    def validate_destination(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute('select des from flight')
        rs=cs.fetchall()
        
        des_list=[]
        des_str=""
        for r in rs:
            r=str(r).split('\'')[1]
            if r not in des_list:
                des_list.append(r)
                
        for d in des_list:
            des_str=des_str+d+", "
            
        slot_value=slot_value.title()  
          
        if slot_value not in des_list:
            dispatcher.utter_message(text="I didn't find any flight to {}, we currently provide flights to {}".format(slot_value, des_str))
            return {"destination": None}
        dispatcher.utter_message(text=f"Ok, your destination is {slot_value}")
        return {"destination": slot_value}
        
    def validate_date(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute('select date from flight')
        rs=cs.fetchall()
        
        date_list=[]
        date_str=""
        for r in rs:
            r=str(r).split('\'')[1]
            if r not in date_list:
                date_list.append(r)
                
        for d in date_list:
            date_str=date_str+d+", "
            
        slot_value=slot_value.title()    
        if slot_value not in date_list:
            dispatcher.utter_message(text="I didn't find any flight to {}, we currently provide flights to {}".format(slot_value, date_str))
            return {"date": None}
        dispatcher.utter_message(text=f"Ok, the date is set to {slot_value}")
        return {"date": slot_value}
    
class ActionQueryFlight(Action):

    def name(self) -> Text:
        return "action_query_flight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dep=tracker.get_slot('departure')
        dest=tracker.get_slot('destination')
        date=tracker.get_slot('date')

        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute("SELECT * FROM flight where dep= '"+dep+ "' AND des= '"+dest+"' AND date='"+date+"'")
        rs=cs.fetchall()

        code=""
        price=""
        msg=""
        
        if len(rs) == 0:
            msg="Sorry, no such flight matched :(. You may try some other dates."
            # print(msg)
        else:
            s=str(rs).split('\'')
            s[8]=s[8].split(' ')[1].split(')')[0]
            msg="There is one matched flight:\n#####################\nDPTR: \t{}\nDEST: \t{}\nCODE: {}\nDATE:\t{}\nPRICE: \t{}".format(s[1],s[3],s[5],s[7],s[8])+"\n#####################\nDo you want to book this flight?"
            code=s[5]
            price=s[8]
    
        dispatcher.utter_message(text=msg)

        return [SlotSet("flightCode",code),SlotSet("price",price)]
    
class ActionSendEmail(Action):
    
    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time=datetime.now().timestamp()
        time=str(time).split('.')[0]+"-"+str(time).split('.')[1]
        
        name=tracker.get_slot('fullname')
        addr=tracker.get_slot('email')
        last_message=tracker.get_intent_of_latest_message
        
        mail="Dear guest,\n\nThank you for contacting us. Our staff will respond to your question as soon as possible.\n\nYour question has been assigned a case number in order to keep track, you can find it below.\n\nBest regards,\nFlyMe Airlines\n\n<text style=\"font-weight:bold;\">Your case:</text>\n------------------------------------------------------------------------------\n<text style=\"font-weight:bold;\">Case number: </text>{}\n\n<text style=\"font-weight:bold;\">Case description: </text>\n<text style=\"font-weight:bold;\">Email address: </text>{} \n<text style=\"font-weight:bold;\">Name: </text>{}\n<text style=\"font-weight:bold;\">Question: </text>{}".format(time,addr,name,last_message)
        
        
        yag=yagmail.SMTP(user='flyme_service_p8@126.com',password='EJAOVZIFXSDCZEID',host='smtp.126.com')
        yag.send(to=addr,subject='Your question regarding flight is received!',contents=mail)
        
        msg="The confirm email is sent, please check. \nIf you don't receive it, please make sure you gave correct email address."
        dispatcher.utter_message(text=msg)

        return []
      
class ActionRegister(Action):
    
    def name(self) -> Text:
        return "action_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code=tracker.get_slot('flightCode')
        id=tracker.get_slot('id')
        fullname=tracker.get_slot('fullname')
        email=tracker.get_slot('email')
        email2=email
        # email=email.split('@')[0]+"'||'&'||'"+email.split('@')[1]
        fullname=fullname.split(' ')[0]+"-"+fullname.split(' ')[1]
        
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        
        cs.execute("SELECT * FROM customer where idnum='"+id+"'")
        rs=cs.fetchall()
        # rc=cs.rowcount()
        print(f"type of rs: {type(rs)}, rs: {rs}")
        # print(f"type of rc: {type(rc)}, rc: {rc}")
        empty_list=[]
        
        if rs == empty_list:            
            cs.execute("insert into customer(fullname, idnum, email) values('"+fullname+"','"+id+"','"+email+"')")
            print("Executed to register: insert into customer(fullname, idnum, email) values('"+fullname+"','"+id+"','"+email+"')")
            cs.close()
            conn.commit()
            conn.close()
            
            msg=""
            rc=cs.rowcount
            if rc > 0:
                fullname=fullname.split('-')[0]+" "+fullname.split('-')[1]
                msg="You seccessfully registered. Please check the information again: \nFullname: \n\t{}\nID:\n\t{}\nEmail: \n\t{}\nType yes to continue to book the flight:".format(fullname,id,email2)
            # DONE TODO: Finish this method
            else:
                msg="Failed to gegister, please contact our staff by saying \"I want staffservice\"."
            dispatcher.utter_message(text=msg)
            
        else:
            cs.close()
            conn.close()
            msg=f"Your ID {id} already exists. Tyep yes to continue to book the flight:"
            dispatcher.utter_message(text=msg)

        return []
    
class ActionOrderFlight(Action):
    
    def name(self) -> Text:
        return "action_order_flight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        code=tracker.get_slot('flightCode')

        id=tracker.get_slot('id')
        price=tracker.get_slot('price')
        dep=tracker.get_slot('departure')
        dest=tracker.get_slot('destination')
        date=tracker.get_slot('date')
        
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
            msg="You seccessfully ordered the ticket. Please check the information again: \nDPTR: \t{}\nDEST:\t{}\nCODE:\t{}\nDATE:\t{}\nPRICE:\t{}".format(dep,dest,code,date,price)
        # DONE TODO: Finish this method


        dispatcher.utter_message(text=msg)
        return []

#TODO: Implement cancel order with service charge (48 hours)
class ActionCancelOrder(Action):

    def name(self) -> Text:
        return "action_cancel_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # code=tracker.get_slot('flightCode')
        id=tracker.get_slot('id')
        code=""
        date0=""
        price=""
        
        """find out the code bought by user FROM TABLE customer"""
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute("SELECT bought_flight FROM customer where idnum='"+id+"'")
        rs=cs.fetchall()
        rc=cs.rowcount
        cs.close()
        conn.close()
        
        for r in rs:
            for i in r:
                
                code=i
        print("bought_flight: "+code)
        
        """set bought_flight as null firstly, then validate"""
        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute("update customer set bought_flight='' where idnum='"+id+"'")
        cs.close()
        conn.commit() 
        conn.close()
        
        if code=="":
            msg="Sorry, you don't have the order, or the ID you provided was incorrect."
        else:
            
            """get date and price from flight table"""
            conn = sqlite3.connect('rasa1.db')
            cs=conn.cursor()
            cs.execute("SELECT date FROM flight where code='"+code+"'") 
            rsD=cs.fetchall() 
            cs.close() 
            conn.close() 
            
            conn = sqlite3.connect('rasa1.db')  
            cs=conn.cursor() 
            cs.execute("SELECT price FROM flight where code='"+code+"'") 
            rsP=cs.fetchall() 
            cs.close()
            conn.close()
            
            for r in rsD:
                for i in r:
                    date0=i
            for r in rsP:
                for i in r:
                    price=i
                    
            print("price: "+str(date0))   
            print("date: "+str(price))    
                    
            today1 = datetime.today().date()  
            print("Today: "+str(today1)) 
            print("The date: "+str(date0))
            date=datetime.strptime(date0,"%Y-%m-%d").date()
            time_interval_day=(date-today1).days
            time_interval_hour=(date-today1).days*24
            
            """jusge if the order is fully refunded"""
            if time_interval_hour >=48:
                msg="You successfully canceled the order of flight {} {} days before it departs. You will get full refund of RMB {}".format(code,time_interval_day,price)
            else:
                price2=str(int(price)*0.8).split('.')[0]
                msg="You seccessfully canceled the order of flight {}, but only {} hours days before it departs. You will get 80% of the full ticket price RMB {}, which is RMB {}.".format(code,time_interval_hour,price,price2)

        dispatcher.utter_message(text=msg)
        return [SlotSet("flightCode",None),SlotSet("price",None)]
    
class ActionFlightList(Action):
    
    def name(self) -> Text:
        return "action_flight_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('rasa1.db')
        cs=conn.cursor()
        cs.execute('select * from flight')
        rs=cs.fetchall()


        list="\n###################################################\n# Currently, we provide the flights listed below: #\n###################################################\n"

        for i in rs:
          s=str(i).split('\'')
          s[8]=s[8].split(' ')[1].split(')')[0]
          strr="{0[1]} -> {0[3]},\t{0[5]},\t{0[7]}, ￥{0[8]}\n".format(s)
          list=list+strr
        cs.close()
        conn.close() 
        
        dispatcher.utter_message(text=list)

        return []
      


