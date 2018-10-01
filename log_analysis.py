#! /usr/bin/env python
# Importing pre defined function 
import psycopg2
DBNAME = "news"


def exet(cmd):
    dbase = psycopg2.connect(database=DBNAME)
    mr = dbase.cursor()
    mr.execute(cmd)
    answer = mr.fetchall()
    dbase.close()
    return answer

# Query To Execute Best Author


def best_author():
    cmd = """select authors.name, count(*)
          as numeric from authors
          join articles
          on authors.id = articles.author
          join log
          on log.path like concat('/article/%',articles.slug)
          group by authors.name
          order by numeric
          desc limit 3; """
    
    result = exet(cmd)
    counts = 1
    print("\nPopular Authors:")
    for n in result:
        print(str(counts) + '.' + n[0] + '--->' + str(n[1]) + " views")
        counts += 1



# Query To Execute Most Errors


def error_terminal():
    cmd = """select tit.day,((erors.er*100)/tit.ers)as prcent
          from ( select date_trunc('day', time) "day", count(*) as er from log
          where status like '404%' group by day) as erors
          join( select date_trunc('day',time) "day", count(*) as ers from log
          group by day) as tit on tit.day =  erors.day
          where (((errors.er*100)/tit.ers)>1)
          order by prcent desc;"""
    result = exet(cmd)
    print("\nMost errors on:")
    for n in result:
        d = n[0].strftime('%B %d, %Y')
        fau = str(n[1]) + "%" + " errors"
        print(d + "--->" + fau)

# Query To Execute Best Article


def best_article():
    cmd = """select articles.title, count(*)
          as numeric from articles
          join log
          on log.path like concat('/article/%',articles.slug)
          group by articles.title
          order by numeric
          desc limit 3;"""

    result = exet(cmd)
    counts = 1
    print("Popular Articles:")
    for n in result:
        nums = str(counts) + '. "'
        topic = n[0]
        vi = '" ---> ' + str(n[1]) + " views"
        print(nums + topic + vi)
        counts += 1


# All 3 Functions Are Called Now
best_article()
best_author()
error_terminal()
