import pymysql
from bs4 import BeautifulSoup
from main.modules.db_set_ditales import host, user, password, db_name
import re

def get_gits_answers(course_id,assignment_id):
    urls=[]
    names_of_users=[]
    id_name_urls = []

    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                select_all_answers_of_assignments = """
                    SELECT mdl_user.firstname,mdl_user.lastname,mdl_assign_submission.userid,mdl_assignsubmission_onlinetext.id,course,name,onlinetext
                    FROM mdl_assign
                    JOIN mdl_assignsubmission_onlinetext 
                    ON mdl_assign.id = mdl_assignsubmission_onlinetext.assignment
                    JOIN mdl_assign_submission
                    ON mdl_assign_submission.id = mdl_assignsubmission_onlinetext.submission
                    JOIN mdl_user 
                    ON  mdl_assign_submission.userid = mdl_user.id
                    WHERE course = %s AND mdl_assign.id = %s   """
                cursor.execute(select_all_answers_of_assignments,(course_id,assignment_id))
                rows = cursor.fetchall()
                for row in rows:
                    names_of_users.append(row['firstname'] +' '+ row['lastname'])
                    soup = BeautifulSoup(row['onlinetext'], 'html.parser')
                    # print(soup.find("a")["href"])
                    comp_name = [link['href'] for link in soup.find_all('a')]
                    if len(comp_name) > 1:
                        
                        link = comp_name[1]
                    else:
                        link = comp_name[0]
                    print(link)
                    id_name_urls.append({'userid': row['userid'],'firstname':row['firstname'],'lastname':row['lastname'],'url': link})
                print("#" * 20)

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

    return id_name_urls

def get_assigns(course_id):
    assigns=[]

    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                select_courses_assign = """
                    SELECT id,name
                    FROM mdl_assign
                    WHERE course = %s;   """
                cursor.execute(select_courses_assign,(course_id))
                assigns = cursor.fetchall()
                print(assigns)

        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

    return assigns