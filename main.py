# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from werkzeug.utils import secure_filename
from PIL import Image

import urllib.request
import urllib.parse


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="price_comparison"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    data2=[]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer")
    dtr1 = mycursor.fetchall()
    for dt1 in dtr1:
        dt2=[]
        mycursor.execute("SELECT * FROM rt_category where retailer=%s",(dt1[6],))
        dtr2 = mycursor.fetchall()
        dt2.append(dt1[1])
        dt2.append(dtr2)
        data2.append(dt2)

    mycursor.execute("SELECT * FROM rt_product order by rand() limit 0,12")
    data1 = mycursor.fetchall()
        
    return render_template('index.html',data2=data2,data1=data1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM rt_retailer WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('rt_home'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg)

@app.route('/login_cus', methods=['GET', 'POST'])
def login_cus():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM rt_customer WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_cus.html',msg=msg)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_admin.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
    
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from rt_customer where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
    
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_customer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO rt_customer(id,name,address,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,address,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('register',act='1'))
        else:
            msg='Already Exist'
    return render_template('register.html',msg=msg,act=act)

@app.route('/reg_retailer', methods=['GET', 'POST'])
def reg_retailer():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
    
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from rt_retailer where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_retailer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO rt_retailer(id,name,address,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,address,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('login'))
        else:
            msg='Already Exist'
    return render_template('reg_retailer.html',msg=msg)

@app.route('/rt_home', methods=['GET', 'POST'])
def rt_home():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_product where retailer=%s",(uname,))
    data2 = mycursor.fetchall()

    if act=="del":
        did = request.args.get('did')
        mycursor.execute("SELECT * FROM rt_product where id=%s",(did,))
        dd = mycursor.fetchone()
        os.remove("static/upload/"+dd[6])
        mycursor.execute('delete from rt_product WHERE id = %s', (did, ))
        mydb.commit()
        return redirect(url_for('rt_home'))
    
    return render_template('rt_home.html',data=data,uname=uname,data2=data2,act=act)



@app.route('/rt_post', methods=['GET', 'POST'])
def rt_post():
    msg=""
    act = request.args.get("act")
    fnn=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM rt_request order by id desc")
    data1 = mycursor.fetchall()

    return render_template('rt_post.html',msg=msg,uname=uname,data=data,data1=data1,act=act)

@app.route('/rt_send', methods=['GET', 'POST'])
def rt_send():
    msg=""
    act = request.args.get("act")
    rid = request.args.get("rid")
    fnn=""
    mess=""
    email=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM rt_request where id=%s",(rid,))
    data1 = mycursor.fetchone()
    cus=data1[1]
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(cus,))
    data2 = mycursor.fetchone()
    email=data2[5]

    
    
        
    if request.method=='POST':
        
        product=request.form['product']
        price=request.form['price']
        
        details=request.form['details']
        
    
        file = request.files['file']
        mycursor.execute("SELECT max(id)+1 FROM rt_reply")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fn=file.filename
            fnn="R"+str(maxid)+fn  
            #fn1 = secure_filename(fn)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fnn))
                
        
        mess="Dear Customer, "+cus+", Your Bid updated by "+uname
        sql = "INSERT INTO rt_reply(id,pid,retailer,product,price,photo,details,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,rid,uname,product,price,fnn,details,'0')
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        msg="success"
        
    
    return render_template('rt_send.html',msg=msg,uname=uname,data=data,data1=data1,act=act,mess=mess,email=email)

@app.route('/rt_view', methods=['GET', 'POST'])
def rt_view():
    msg=""
    cnt=0
    uname=""
    
    act = request.args.get('act')
    rid = request.args.get('rid')
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    usr = mycursor.fetchone()


    mycursor.execute("SELECT * FROM rt_reply where id=%s order by id ",(rid,))
    data = mycursor.fetchall()
    
    return render_template('rt_view.html',msg=msg,usr=usr,data=data,rid=rid)

@app.route('/rt_book', methods=['GET', 'POST'])
def rt_book():
    msg=""
    cnt=0
    uname=""
    
    act = request.args.get('act')
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    


    mycursor.execute("SELECT * FROM rt_request where status=1 && retailer=%s order by id desc ",(uname,))
    data = mycursor.fetchall()
    
    return render_template('rt_book.html',msg=msg,usr=usr,data=data)
@app.route('/search1', methods=['GET', 'POST'])
def search1():
    msg=""
    searchdata=request.args.get("searchdata")
    return render_template('search1.html',msg=msg,searchdata=searchdata)
@app.route('/rt_info', methods=['GET', 'POST'])
def rt_info():
    msg=""
    cnt=0
    uname=""
    
    act = request.args.get('act')
    rid = request.args.get('rid')
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    
    if request.method=='POST':
        details=request.form['details']

        mycursor.execute("update rt_request set details=%s where id=%s",(details,rid))
        mydb.commit()
        msg="success"
    
    return render_template('rt_info.html',msg=msg,usr=usr)

@app.route('/rt_sales', methods=['GET', 'POST'])
def rt_sales():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_cart c,rt_product p where c.pid=p.id && c.status=1 && p.retailer=%s",(uname,))
    data2 = mycursor.fetchall()


    
    return render_template('rt_sales.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    msg=""
    act = request.args.get("act")
    fnn=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
        
    if request.method=='POST':
        category=request.form['category']

        mycursor.execute("SELECT max(id)+1 FROM rt_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO rt_category(id,retailer,category) VALUES (%s, %s, %s)"
        val = (maxid,uname,category)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        result="sucess"
        if mycursor.rowcount==1:
            return redirect(url_for('add_cat',act='1'))
        else:
            msg='Already Exist'

    if act=="del":
        did = request.args.get('did')
        mycursor.execute('delete from rt_category WHERE id = %s', (did, ))
        mydb.commit()
        return redirect(url_for('add_cat'))

    
        
    mycursor.execute("SELECT * FROM rt_category where retailer=%s",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('add_cat.html',msg=msg,uname=uname,data=data,data2=data2,act=act)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    msg=""
    act = request.args.get("act")
    fnn=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM rt_category where retailer=%s",(uname,))
    data1 = mycursor.fetchall()

    
        
    if request.method=='POST':
        category=request.form['category']
        product=request.form['product']
        price=request.form['price']
        qty=request.form['qty']
        details=request.form['details']
        
    
        file = request.files['file']
        mycursor.execute("SELECT max(id)+1 FROM rt_product")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fn=file.filename
            fnn="P"+str(maxid)+fn  
            #fn1 = secure_filename(fn)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fnn))
                
        
        
        sql = "INSERT INTO rt_product(id,retailer,category,product,price,quantity,photo,details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,category,product,price,qty,fnn,details)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        result="sucess"
        if mycursor.rowcount==1:
            return redirect(url_for('add_product',act='1'))
        else:
            msg='Already Exist'

    

    
        
    mycursor.execute("SELECT * FROM rt_product")
    data2 = mycursor.fetchall()
    
    return render_template('add_product.html',msg=msg,uname=uname,data=data,data1=data1,act=act)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    pid=request.args.get("pid")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
    data2 = mycursor.fetchone()

    if request.method=='POST':
        product=request.form['product']
        price=request.form['price']
        qty=request.form['qty']
        details=request.form['details']
        mycursor.execute("update rt_product set product=%s,price=%s,quantity=%s,details=%s where id=%s",(product,price,qty,details,pid))
        mydb.commit()

        mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
        dd3 = mycursor.fetchone()
        if dd3[5]>dd3[9]:
            mycursor.execute("update rt_product set status=0 where id=%s",(pid,))
            mydb.commit()
    
        return redirect(url_for('rt_home'))
        
    
    return render_template('edit.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/search', methods=['GET', 'POST'])
def search():
    msg=""
    cnt=0
    uname=""
    data=[]
    mess=""
    email=""
    st=""
    show=""
    searchdata = request.args.get('searchdata')
    act = request.args.get('act')
    bt = request.args.get('bt')
    cat = request.args.get('cat')
    mycursor = mydb.cursor()

    data2=[]
    mycursor.execute("SELECT * FROM rt_retailer")
    dtr1 = mycursor.fetchall()
    for dt1 in dtr1:
        dt2=[]
        mycursor.execute("SELECT * FROM rt_category where retailer=%s",(dt1[6],))
        dtr2 = mycursor.fetchall()
        dt2.append(dt1[1])
        dt2.append(dtr2)
        data2.append(dt2)

    cc=""
    if cat is None:
        cc=""
    else:
        cc="1"
    ####
    if act=="ct":
        rt=request.args.get("rt")
        mycursor.execute("SELECT * FROM rt_product where category=%s && retailer=%s",(cat,rt))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
    ####
    elif bt=="1":
        show="1"
        getval=searchdata
        cat="%"+getval+"%"
        prd="%"+getval+"%"
        det="%"+getval+"%"
        mycursor.execute("SELECT * FROM rt_product where category like %s || product like %s || details like %s",(cat,prd,det))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)

    else:
        mycursor.execute("SELECT * FROM rt_product order by rand() limit 0,12")
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
    
    return render_template('search.html',msg=msg,data=data,cnt=cnt,data2=data2,st=st,show=show,searchdata=searchdata)


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    uname=""
    
    act = request.args.get('act')
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    
    if request.method=='POST':
        product=request.form['product']
        mycursor.execute("SELECT max(id)+1 FROM rt_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        sql = "INSERT INTO rt_request(id, uname, product) VALUES (%s, %s, %s)"
        val = (maxid, uname, product )
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"

    mycursor.execute("SELECT * FROM rt_request where uname=%s order by id desc",(uname,))
    data = mycursor.fetchall()
    
    return render_template('userhome.html',msg=msg,usr=usr,data=data)


@app.route('/search11', methods=['GET', 'POST'])
def search11():
    msg=""
    cnt=0
    uname=""
    data=[]
    mess=""
    email=""
    st=""
    act = request.args.get('act')
    bt = request.args.get('bt')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0', (uname,))
    cart_n = mycursor.fetchone()[0]


    data2=[]
    mycursor.execute("SELECT * FROM rt_retailer")
    dtr1 = mycursor.fetchall()
    for dt1 in dtr1:
        dt2=[]
        mycursor.execute("SELECT * FROM rt_category where retailer=%s",(dt1[6],))
        dtr2 = mycursor.fetchall()
        dt2.append(dt1[1])
        dt2.append(dtr2)
        data2.append(dt2)

    cc=""
    if cat is None:
        cc=""
    else:
        cc="1"
    ####
    if act=="ct":
        rt=request.args.get("rt")
        mycursor.execute("SELECT * FROM rt_product where category=%s && retailer=%s",(cat,rt))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
    ####
    elif bt=="1":
        getval=request.args.get("getval")
        cat="%"+getval+"%"
        prd="%"+getval+"%"
        det="%"+getval+"%"
        mycursor.execute("SELECT * FROM rt_product where category like %s || product like %s || details like %s",(cat,prd,det))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)

    else:
        mycursor.execute("SELECT * FROM rt_product order by rand() limit 0,12")
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
            

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    if act=="cart":
        pid = request.args.get('pid')
        mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && pid = %s && status=0', (uname, pid))
        num = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
        pdata = mycursor.fetchone()
        price=pdata[4]
        cat=pdata[3]
        retailer=pdata[1]
        if num==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_cart")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO rt_cart(id, uname, pid, status, rdate, price,category, retailer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, uname, pid, '0', rdate, price, cat, retailer)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('userhome',act='mail',prid=str(pid)))

    mycursor.execute("SELECT count(*) FROM rt_cart where uname=%s && status=0",(uname,))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        msg="1"
    else:
        msg=""

    if act=="mail":
        prid=request.args.get("prid")
        mycursor.execute('SELECT count(*) FROM rt_product WHERE id=%s && status=0 && quantity<5',(prid,))
        nn = mycursor.fetchone()[0]
        if nn>0:
            st="1"
            mycursor.execute('SELECT * FROM rt_product WHERE id=%s && status=0 && quantity<5',(prid,))
            dd = mycursor.fetchone()

            mess="Product ID"+str(prid)+", Product:"+dd[3]+", Low Quantity "+str(dd[5])

            mycursor.execute("update rt_product set status=1 where id=%s ",(prid,))
            mydb.commit()
            
            mycursor.execute('SELECT * FROM rt_retailer WHERE uname=%s',(dd[1],))
            pd1 = mycursor.fetchone()
            email=pd1[5]
            print("mail sent "+email)
        
        
    
    return render_template('search11.html',msg=msg,uname=uname,usr=usr,data=data,cnt=cnt,data2=data2,cart_n=cart_n,st=st,mess=mess,email=email)

@app.route('/view_bid', methods=['GET', 'POST'])
def view_bid():
    msg=""
    cnt=0
    uname=""
    
    act = request.args.get('act')
    pid = request.args.get('pid')
    rid = request.args.get('reply_id')
    retailer = request.args.get('retailer')
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    if act=="book":
        
    
        mycursor.execute("update rt_request set status=1,retailer=%s,reply_id=%s where id=%s ",(retailer,rid,pid))
        mydb.commit()
        mycursor.execute("update rt_reply set status=1 where id=%s ",(rid,))
        mydb.commit()
        msg="success"


    mycursor.execute("SELECT * FROM rt_reply where pid=%s order by id ",(pid,))
    data = mycursor.fetchall()
    
    return render_template('view_bid.html',msg=msg,usr=usr,data=data,pid=pid,rid=rid,retailer=retailer)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    msg=""
    uname=""
    act=request.args.get("act")
    st=""
    pid=""
    did=""
    total=0
    amount=""
    pdata=[]
    pdata1=[]
    mess=""
    email=""
            
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    email=usr[5]
    name=usr[1]

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0', (uname,))
    cart_n = mycursor.fetchone()[0]

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
    cn = mycursor.fetchone()[0]
    if cn>0:
        mycursor.execute('SELECT sum(amount) FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
        total = mycursor.fetchone()[0]

    mycursor.execute("SELECT distinct(category) FROM rt_category")
    data2 = mycursor.fetchall()
    
    mycursor.execute("SELECT count(*) FROM rt_cart where uname=%s && status=0",(uname, ))
    cnt = mycursor.fetchone()[0]
    
    
    mycursor.execute('SELECT c.id,p.product,p.price,p.details,p.photo,c.rdate,c.quantity,c.amount,c.check_st,av_product FROM rt_cart c,rt_product p where c.pid=p.id and c.uname=%s and c.status=0', (uname, ))
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM rt_cart where uname=%s && status=0",(uname, ))
    dr = mycursor.fetchall()

        
    i=0
    mul=0
    if request.method=='POST':
        ch=request.form['ch']
        
        qty=request.form.getlist('qty[]')
        rid=request.form.getlist('rid[]')

        if ch=="1":

            mycursor.execute("update rt_cart set check_st=0,av_product=0 where uname=%s && status=0",(uname, ))
            mydb.commit()
        
            for d1 in rid:
                user_qty=int(qty[i])

                
                
                mycursor.execute("SELECT price FROM rt_cart where id=%s",(d1, ))
                d2 = mycursor.fetchone()[0]
                mul=d2*user_qty

                mycursor.execute("SELECT * FROM rt_cart where id=%s",(d1, ))
                d3 = mycursor.fetchone()
                prid=d3[2]

                                
                mycursor.execute("SELECT * FROM rt_product where id=%s",(prid, ))
                pr = mycursor.fetchone()
                pr_qty=pr[5]
                
                

                rqty=pr[9]-d3[7]
                av_qty=pr_qty-rqty
                
                rqty1=rqty+user_qty
                mycursor.execute("update rt_product set required_qty=%s where id=%s ",(rqty1,prid))
                mydb.commit()

                if av_qty<user_qty:
                    mycursor.execute("update rt_cart set check_st=1,av_product=%s where id=%s && pid=%s",(av_qty,d1,prid))
                    mydb.commit()
                    
                
                mycursor.execute("update rt_cart set quantity=%s,amount=%s where id=%s ",(user_qty,mul,d1))
                mydb.commit()
                i+=1

                
            return redirect(url_for('cart',act='mail'))
        elif ch=="2":
            print("buy")
            if total>0:
                return redirect(url_for('cart',act='otp'))
            else:
                msg="2"
        elif ch=="3":
            print("check otp")
            otp=request.form['otp']
            mycursor.execute('SELECT * FROM rt_customer WHERE uname=%s',(uname,))
            r1 = mycursor.fetchone()
            if r1[9]==otp:
                return redirect(url_for('cart',act='yes'))
            else:
                msg="4"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute('SELECT * FROM rt_cart WHERE id=%s',(did,))
        dd1 = mycursor.fetchone()
        pid1=dd1[2]
        mycursor.execute("update rt_product set required_qty=required_qty-%s where id=%s",(dd1[7],pid1))
        mydb.commit()
        mycursor.execute("delete from rt_cart where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('cart'))
        
    #send mail for products required  
    if act=="mail":
        print("mail")
        mycursor.execute('SELECT count(*) FROM rt_product WHERE required_qty>quantity && status=0')
        pn = mycursor.fetchone()[0]

        
        if pn>0:
            st="1"
           
            mycursor.execute('SELECT * FROM rt_product WHERE required_qty>quantity && status=0')
            pdata = mycursor.fetchall()

            for rr in pdata:
                dt=[]
                ret=rr[1]
                mycursor.execute('SELECT * FROM rt_retailer WHERE uname=%s',(ret,))
                pd1 = mycursor.fetchone()

                pname=rr[3]
                pid=rr[0]
                email=pd1[5]
                avp=rr[5]
                rp=rr[9]

                mess="Product ID: "+str(pid)+", Product: "+pname+", Availble only "+str(avp)+", Required "+str(rp)
                mycursor.execute("update rt_product set status=1 where id=%s ",(rr[0],))
                mydb.commit()
                    
                dt.append(mess)
                dt.append(email)
                pdata1.append(dt)
            

    if act=="otp":
        rn=randint(1000,9999)
        mess="OTP: "+str(rn)
        mycursor.execute("update rt_customer set otp=%s where uname=%s",(str(rn),uname))
        mydb.commit()
        
        
    #payment
    if act=="yes":

        mycursor.execute('SELECT * FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
        qc = mycursor.fetchall()
        for rc in qc:
            uq=rc[7]
            mycursor.execute("update rt_product set quantity=quantity-%s,required_qty=required_qty-%s where id=%s",(uq,uq,rc[2]))
            mydb.commit()
        
        mycursor.execute("SELECT max(id)+1 FROM rt_purchase")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        mycursor.execute('update rt_cart set status=1,bill_id=%s WHERE uname=%s && status=0 && check_st=0', (maxid, uname ))
        mydb.commit()

        sql = "INSERT INTO rt_purchase(id, uname, amount, rdate) VALUES (%s, %s, %s, %s)"
        val = (maxid, uname, total, rdate)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('cart', act='success'))
    if act=="success":
        mycursor.execute('SELECT amount FROM rt_purchase WHERE uname=%s order by id desc limit 0,1', (uname,))
        amount = mycursor.fetchone()[0]
        mess="Dear "+name+", Amount Rs."+str(amount)+" Purchased Success"
        msg="3"

    '''if request.method=='POST':
        amount=request.form['amount']
        print("test")
        return redirect(url_for('payment', amount=amt))'''
            
    return render_template('cart.html',msg=msg,uname=uname,usr=usr,data=data,cnt=cnt,data2=data2,cart_n=cart_n,total=total,act=act,pdata1=pdata1,st=st,mess=mess,email=email)



@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    uname=""
    act=request.args.get("act")
    data2=[]
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    
    
    mycursor.execute("SELECT * FROM rt_purchase where uname=%s",(uname, ))
    data1=mycursor.fetchall()

    if act=="view":
        rid=request.args.get("rid")
        mycursor.execute("SELECT * FROM rt_cart where uname=%s &&bill_id=%s",(uname,rid))
        data2=mycursor.fetchall()

        
    return render_template('purchase.html',usr=usr,uname=uname,data1=data1,act=act,data2=data2)

@app.route('/view', methods=['GET', 'POST'])
def view():
    uname=""
    amount=0
    if 'username' in session:
        uname = session['username']
    
    bid = request.args.get('bid')
    cursor = mydb.cursor()
    cursor.execute('SELECT c.id,p.product,p.price,p.detail,p.photo,c.rdate FROM rt_cart c,rt_product p where c.pid=p.id and c.bill_id=%s', (bid, ))
    data = cursor.fetchall()

    return render_template('view.html', data=data)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer")
    data = mycursor.fetchall()

    if act=="yes":
        did=request.args.get("did")
        mycursor.execute("update rt_retailer set status=1 where id=%s",(did,))
        mydb.commit()
        return redirect(url_for("admin"))
    return render_template('admin.html',data=data)

##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


