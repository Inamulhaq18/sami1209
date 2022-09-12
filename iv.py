import streamlit as st
from PIL import Image as PILImage
import logging
import os
from pupdatabase import update_product
from abo5s3 import *
import time
import datetime
import requests
from categories import *


def imageprocessapi(links):
    session = requests.Session()
    session.trust_env = False
    links=links
    url="https://abo5imageapi.herokuapp.com/processBG?rurl="
    url=url+links
    response = session.get(url)
    print(response.content)

def generatedesc(productname):
    session = requests.Session()
    session.trust_env = False
    url="https://abo5describtionapi.herokuapp.com/generate?productname="
    url=url+productname
    response = session.get(url)
    print(response.content)

url="https://abo5.s3.eu-central-1.amazonaws.com/"
#create a subheading 
name="Waleed"
st.header("Hi, " + name + "😃")
#product name 
productname_en=st.text_input("Product Name Enlish : ", "",key="productnameen" )
#productname_ar=st.text_input("Product Name Arabic : ")
productname_ar=""
#tags=st.text_input("Tags : ").split(",")
tags=""
shape=st.selectbox("Select Shape/Materials : " , ['Select','Square','Rectangle','Circle','Triangle','Semi-Circle','others'],key="catsize")
if shape=="others":
   shape=st.text_input("Please mention the shape")

sizecolor=st.selectbox("Select Size/Color : " , ["Select",'Size','Color'],key="catshape")
if sizecolor=='Size':
   sizecolor=st.multiselect("Select size", ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL"],key="line")
if sizecolor=='Color':
   sizecolor=st.multiselect("Select color",["red", "blue", "green", "yellow", "black", "white","Pink","transparent","Translucent"],key="line45")
alsoknownas=st.text_input("Other Names : " , key="othername")
if shape!='Select':
    tags='''
Shape/Materials : 
{}
    '''.format(shape)
if sizecolor != 'Select':
    tags=tags+'''

Size/Color: 
{}'''.format(",".join(sizecolor))

if alsoknownas!="":
    tags=tags+'''
    Also known as:
    {}'''.format(alsoknownas)
category=st.selectbox("Select a Category : " , categories1.keys(),key="cat")
sub_cat=st.selectbox("Select a Sub-Category : " , categories1[category],key="subcat")
store=st.selectbox("Select Store : ",['Alam-at tawfeeq', 'World of Saving',"other"])
price=st.number_input("Price : ",5.75)


uploaded_files=st.file_uploader("Upload a file", type=["png", "jpg", "jpeg"], accept_multiple_files=True) 
st.write(len(uploaded_files))
lst = list(range(1,len(uploaded_files)+1))
###############################varient1
images=[]
for uploaded_file in uploaded_files:
    img1 = PILImage.open(uploaded_file)
    images.append(img1)
st.image(images,width=150,caption=lst)


###############################varient
varient={}
with st.expander("Varient", expanded=True):
    if len (uploaded_files)>0:

        typev2=st.selectbox("Select varient type", ["Select","size", "color", "design"],key="type")
        ######################size
        varient={"type":typev2}
        if typev2 == "size":
            datav2=st.multiselect("Select size", ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL","others1","others2","others3","others4"],key="size")
            #st.write(datav2[0])
            varient["data"]=datav2
            if "S" in datav2:
                s_image=st.multiselect("Select Images for S", lst,key="S")
                varient["S_img"]=s_image

            if "M" in datav2:
                m_image=st.multiselect("Select Images for M", lst,key="M")
                varient["M_img"]=m_image

            if "L" in datav2:
                l_image=st.multiselect("Select Images for L", lst,key="L")    
                varient["L_img"]=l_image
            if "XL" in datav2:
                xl_image=st.multiselect("Select Images for XL", lst,key="XL")          
                varient["XL_img"]=xl_image
            if "XXL" in datav2:
                xxl_image=st.multiselect("Select Images for XXL", lst,key="XXL")      
                varient["XXL_img"]=xxl_image
            if "XXXL" in datav2:
                xxxl_image=st.multiselect("Select Images for XXXL", lst,key="XXXL")     
                varient["XXXL_img"]=xxxl_image
            if "XXXXL" in datav2:
                xxxxl_image=st.multiselect("Select Images for XXXXL", lst,key="XXXXL")     
                varient["XXXXL_img"]=xxxxl_image
            if "others1" in datav2:
                others1_size_name=st.text_input("Enter name for others1 : ")
                others1_size_image=st.multiselect("Select Images for others1", lst,key="others1") 
                others1={"others1_img":others1_size_image,"others1_name":others1_size_name}
                varient["others1"]=others1
           
            if "others2" in datav2:
                others2_size_name=st.text_input("Enter name for others2 : ")
                others2_size_image=st.multiselect("Select Images for others2", lst,key="others2")
                others2={"others2_img":others2_size_image,"others2_name":others2_size_name}
                varient["others2"]=others2

            if "others3" in datav2:
                others3_size_name=st.text_input("Enter name for others3 : ")
                others3_size_image=st.multiselect("Select Images for others3", lst,key="others3") 
                others3={"others3_img":others3_size_image,"others3_name":others3_size_name}
                varient["others3"]=others3

            if "others4" in datav2:
                others4_size_name=st.text_input("Enter name for others4 : ")
                others4_size_image=st.multiselect("Select Images size others4", lst,key="others4")
                others4={"others4_img":others4_size_image,"others4_name":others4_size_name}
                varient["others4"]=others4
                

        if typev2 == "color":
            
            datav2=st.multiselect("Select color", ["red", "blue", "green", "yellow", "black", "white","transparent",
                                "Translucent","Multicolor", "others1","others2","others3","others4"],key="color")
            varient["data"]=datav2
            if "red" in datav2:
                red_image=st.multiselect("Select Images for red", lst,key="red")
                varient["red_img"]=red_image

            if "blue" in datav2:
                blue_image=st.multiselect("Select Images for blue", lst,key="blue")
                varient["blue_img"]=blue_image

            if "green" in datav2:
                green_image=st.multiselect("Select Images for green", lst,key="green")  
                varient["green_img"]=green_image  

            if "yellow" in datav2:
                yellow_image=st.multiselect("Select Images for yellow", lst,key="yellow")
                varient["yellow_img"]=yellow_image       

            if "black" in datav2:
                black_image=st.multiselect("Select Images for black", lst,key="black")      
                varient["black_img"]=black_image
            if "white" in datav2:
                white_image=st.multiselect("Select Images for white", lst,key="white")     
                varient["white_img"]=white_image
            if "transparent" in datav2:
                transparent_image=st.multiselect("Select Images for transparent", lst,key="transparent")     
                varient["transparent_img"]=transparent_image
            if "Translucent" in datav2:
                translucent_image=st.multiselect("Select Images for Translucent", lst,key="translucent")  
                varient["translucent_img"]=translucent_image
            if "Multicolor" in datav2:
                multicolor_image=st.multiselect("Select Images for Multicolor", lst,key="multicolor")    
                varient["multicolor_img"]=multicolor_image
            
            if "others1" in datav2:
                other1_color_name=st.text_input("Enter name for others1 : ")
                other1_color_image=st.multiselect("Select Images for others1", lst,key="others1") 
                otherc1={"otherc1_img":other1_color_image,"otherc1_name":other1_color_name}
                varient["otherc1"]=otherc1
            
            if "others2" in datav2:
                other2_color_name=st.text_input("Enter name for others2 : ")
                other2_color_image=st.multiselect("Select Images for others2", lst,key="others2") 
                otherc2={"otherc2_img":other2_color_image,"otherc2_name":other2_color_name}
                varient["otherc2"]=otherc1

            if "others3" in datav2:
                other3_color_name=st.text_input("Enter name for others3 : ")
                other3_color_image=st.multiselect("Select Images for others3", lst,key="others3") 
                otherc3={"otherc3_img":other3_color_image,"otherc3_name":other3_color_name}
                varient["otherc3"]=otherc3
            if "others4" in datav2:
                other4_color_name=st.text_input("Enter name for others4 : ")
                other4_color_image=st.multiselect("Select Images size others4", lst,key="others4") 
                otherc4={"otherc4_img":other4_color_image,"otherc4_name":other4_color_name}
                varient["otherc4"]=otherc4

        if typev2 == "design":
            datav2=st.multiselect("Select Design", ["Design1","Design2","Design3","Design4","Design5"],key="design")
            if "Design1" in datav2:
                other1_design_name=st.text_input("Enter name for Design1 : ")
                other1_design_image=st.multiselect("Select Images for Design1", lst,key="design1")
                otherd1={"otherd1_img":other1_design_image,"otherd1_name":other1_design_name}
                varient["otherd1"]=otherd1
            if "Design2" in datav2:
                other2_design_name=st.text_input("Enter name for Design2 : ")
                other2_design_image=st.multiselect("Select Images for Design2", lst,key="deisgn2")
                otherd2={"otherd2_img":other2_design_image,"otherd2_name":other2_design_name}
                varient["otherd2"]=otherd2
            if "Design3" in datav2:
                other3_design_name=st.text_input("Enter name for Design3 : ")
                other3_design_image=st.multiselect("Select Images for Design3", lst,key="design3")
                otherd3={"otherd3_img":other3_design_image,"otherd3_name":other3_design_name}
                varient["otherd3"]=otherd3
            if "Design4" in datav2:
                other4_design_name=st.text_input("Enter name for Design4 : ")
                other4_design_image=st.multiselect("Select Images for Design4", lst,key="design4")
                otherd4={"otherd4_img":other4_design_image,"otherd4_name":other4_design_name}
                varient["otherd4"]=otherd4
            if "Design5" in datav2:
                other5_design_name=st.text_input("Enter name for Design5 : ")               
                other5_design_image=st.multiselect("Select Images for Design5", lst,key="design5")
                otherd5={"otherd5_img":other5_design_image,"otherd5_name":other5_design_name}
                varient["otherd5"]=otherd5
            #st.write(datav2[0])
#st.write(varient)

linksp=""
#sumbit button
urllist=[]
if st.button("Submit"):
    if productname_en=="" or len(uploaded_files)==0:
        st.header("😡 HEYYYY! Product Name and Images_uploaded cannot be empty !")
    else:
        with st.spinner('Wait for it...'):
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                name=save_uploadedfile(uploaded_file)
                #st.write(name)
                #upload R to s3

                s3.Bucket('abo5').upload_file(Filename=name, Key=name)
                urllist.append(url+name)
            links = ", ".join(urllist)
            status=update_product(Product_Entry_Timestamp=datetime.datetime.now(), Product_Name_en=productname_en,
                            Product_Name_ar=productname_ar, Product_Category=category,Tags=tags,Retail_outlet=store,
                            Product_price=price, Product_image_R_url=links, Product_image_P_url=linksp,user="Waleed",Product_subcategory=sub_cat, variety=varient) 
            st.success("Updated")
            time.sleep(1)
            imageprocessapi(links)#processing the raw image heroku server
            st.write("Image Process Server.....")
            generatedesc(productname_en)
            st.write("describtion gen Server.....")


            st.write(f'''
              <a target="_self" href="https://inamulhaq18-waleed-varient2-iv-g9mop1.streamlitapp.com/">
                  <button>
                      Reload
                  </button>
              </a>
              ''',
              unsafe_allow_html=True
            )
