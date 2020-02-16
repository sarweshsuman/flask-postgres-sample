import psycopg2
import json

class TicketsPostgresWrapper:
    connect_string="dbname='postgres' user='postgres' host='localhost' password='postgres'  port = 5432"
    query_all_data = "SELECT * from api.tickets"
    insert_all_data = "insert into api.tickets values (3,'test','test','test','test') "
    def __init__(self):
        try:
            self.conn = psycopg2.connect(self.connect_string)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("I am unable to connect to the database ",e)
    def close1(self):
        try:
            self.conn.close1()
        except Exception as e:
            print("Got error while disconnecting {}".format(e))

    def get_all_rows1(self):
        try:
            data=[]
            self.cursor.execute(self.query_all_data)
            rows = self.cursor.fetchall()
            for row in rows:
                data.append(row)
            return data
        except Exception as e:
            print("Error occurred while trying to get data ",e)

    def get_issue_details(self,ticket_no):
        try:
            data=[]
            self.cursor.execute("select issue_details from api.tickets where ticket_no="+str(ticket_no))
            rows = self.cursor.fetchall()
            for row in rows:
                data.append(row)
            return data
        except Exception as e:
            print("Error occurred while trying to get data ",e)

    def get_suggested_assignment_group(self,ticket_no):
        try:
            data=[]
            self.cursor.execute("select suggested_assignment_group from api.tickets where ticket_no="+str(ticket_no))
            rows = self.cursor.fetchall()
            for row in rows:
                data.append(row)
            return data
        except Exception as e:
            print("Error occurred while trying to get data ",e)

    def get_tickets_with_unknown_suggested_assignment_group(self):
        try:
            data=[]
            self.cursor.execute("select ticket_no from api.tickets where suggested_assignment_group = 'unknown' order by ticket_no desc")
            rows = self.cursor.fetchall()
            for row in rows:
                data.append(row)
            return data
        except Exception as e:
            print("Error occurred while trying to get data ",e)

    def get_tickets_with_known_suggested_assignment_group_and_unknown_suggested_rca(self):
        try:
            data=[]
            self.cursor.execute("select ticket_no from api.tickets where suggested_assignment_group != 'unknown' and suggested_assignment_group != 'Processing' and suggested_rca = 'unknown' order by ticket_no desc")
            rows = self.cursor.fetchall()
            for row in rows:
                data.append(row)
            return data
        except Exception as e:
            print("Error occurred while trying to get data ",e)

    def insert_data(self,dict):
        try:
            self.cursor.execute('INSERT INTO api.tickets (ticket_no,assignment_group,issue_details,suggested_assignment_group,suggested_rca) VALUES (%s,%s,%s,%s,%s)', (dict['ticket_no'],dict['assignment_group'],dict['issue_details'],dict['suggested_assignment_group'],dict['suggested_rca']))
            self.conn.commit();
        except Exception as e:
            print("Error occurred while trying to insert data ",e)
    def update_suggested_assignment_group(self,ticket_no,status):
        try:
            self.cursor.execute("UPDATE api.tickets SET suggested_assignment_group ='"+status+"' WHERE ticket_no="+str(ticket_no) )
            self.conn.commit();
        except Exception as e:
            print("Error occurred while trying to update suggested_assignment_group ",e)
    def update_suggested_rca(self,ticket_no,status):
        try:
            self.cursor.execute("UPDATE api.tickets SET suggested_rca='"+status+"' WHERE ticket_no="+str(ticket_no) )
            self.conn.commit();
        except Exception as e:
            print("Error occurred while trying to update suggested_assignment_group ",e)

if __name__ == '__main__':
    ticket_postgres = TicketsPostgresWrapper();
    ticket_postgres.insert_data(json.loads('{"ticket_no": 3,"assignment_group": "unknown","issue_details": "hello this is your issue","suggested_assignment_group": "unknown","suggested_rca": "unknown"}'))
