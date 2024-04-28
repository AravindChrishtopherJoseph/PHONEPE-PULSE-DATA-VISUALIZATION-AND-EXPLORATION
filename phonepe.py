import streamlit as st
from streamlit_option_menu  import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#SQL connection

mydb= psycopg2.connect(host="localhost",
                       user= 'postgres',
                       database="phonepe-dataset",
                       password="Aravind#123",
                       port="5432")
cursor=mydb.cursor()

#aggre_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1, columns=("States", "Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))   


#aggre_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2, columns=("States", "Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))



#aggregated_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("States", "Years", "Quarter","Brands","Transaction_count","Percentage"))


#map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4, columns=("States", "Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5, columns=("States", "Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6, columns=("States", "Years", "Quarter","Districts","RegisteredUsers","AppOpens"))


#top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7, columns=("States", "Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))


#top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8, columns=("States", "Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9, columns=("States", "Years", "Quarter","Pincodes","RegisteredUsers"))




def Transaction_amount_count_Y(df, year):

    tacy=df[df["Years"]==year]
    tacy.reset_index(drop= True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

      fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f" {year} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset, height= 650, width= 600)
      st.plotly_chart(fig_amount)

    with col2:

      fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f" {year} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.amp_r, height= 650, width= 600)
      st.plotly_chart(fig_count)

    col1,col2= st.columns(2) 
    with col1:

      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

      response=requests.get(url)

      data1=json.loads(response.content)

      states_name=[]
      for feature in data1["features"]:
         states_name.append(feature["properties"]["ST_NM"])

      states_name.sort()

      fig_india_1=px.choropleth (tacyg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_amount", color_continuous_scale="viridis", range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                 hover_name ="States", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",height= 600, width= 600 )
      fig_india_1.update_geos(visible=False)
      
      st.plotly_chart(fig_india_1)

    with col2:  

      fig_india_2=px.choropleth (tacyg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_count", color_continuous_scale="viridis", range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                 hover_name ="States", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",height= 600, width= 600 )
      fig_india_2.update_geos(visible=False)
      
      st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):

    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop= True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

      fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f" {tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset,height= 650, width= 600)
      st.plotly_chart(fig_amount)

    with col2:

      fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f" {tacy ['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.amp_r,height= 650, width= 600)
      st.plotly_chart(fig_count)

    col1,col2=st.columns(2)  

    with col1:

      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

      response=requests.get(url)

      data1=json.loads(response.content)

      states_name=[]
      for feature in data1["features"]:
         states_name.append(feature["properties"]["ST_NM"])

      states_name.sort()

      fig_india_1=px.choropleth (tacyg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_amount", color_continuous_scale="viridis", range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                 hover_name ="States", title=f" {tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",height= 600, width= 600 )
      fig_india_1.update_geos(visible=False)
      
      st.plotly_chart(fig_india_1)

    with col2:

      fig_india_2=px.choropleth (tacyg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_count", color_continuous_scale="viridis", range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                 hover_name ="States", title=f"{tacy ['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",height= 600, width= 600 )
      fig_india_2.update_geos(visible=False)
      
      st.plotly_chart(fig_india_2)

    return tacy 

def Aggre_Tran_Transaction_type(df,state):

   tacy=df[df["States"]==state]
   tacy.reset_index(drop= True, inplace=True)	

   tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
   tacyg.reset_index(inplace=True)

   col1,col2= st.columns(2)
   with col1:

      fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type", values="Transaction_amount",width=600, title=f" {state.upper()} TRANSACTION AMOUNT")

      st.plotly_chart(fig_pie_1)

   with col2:   

      fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type", values="Transaction_count",width=600, title=f" {state.upper()} TRANSACTION COUNT")

      st.plotly_chart(fig_pie_2) 


 #Agrregated_User_analysis_year

def Aggre_user_plot_1(df,year):

    aguy=df[df["Years"]==year]

    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())

    aguyg.reset_index(inplace=True)                            

    fig_bar_1=px.bar(aguyg,x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",width=700, color_discrete_sequence=px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_1)

    return aguy  

#Aggre_user_analysis_quarter

def Aggre_user_plot_2(df,quarter):

    aguyq=df[df["Quarter"]== quarter]

    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")[["Transaction_count"]].sum())

    aguyqg.reset_index(inplace=True) 

    fig_bar_1=px.bar(aguyqg,x="Brands", y="Transaction_count", title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",width=700, color_discrete_sequence=px.colors.sequential.ice_r)

    st.plotly_chart(fig_bar_1)

    return aguyq
   
#Agrregated_User_analysis_States

def Agrre_user_plot_3(df,state):

    auyqs=df[df["States"]== state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_scatter_1= px.scatter(auyqs, x= "Brands", y="Transaction_count", hover_data="Percentage", title=f"{state.upper()} BRANDS,TRANSACTION COUNT,AND PERCENTAGE", width=800)

    st.plotly_chart(fig_scatter_1)

#Map_Insurance_District

def Map_Insur_District(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop= True, inplace=True)	

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_bar_1=px.bar(tacyg,y="Districts", x="Transaction_amount", orientation= "h", title=f" {state.upper()} STATE DISTRICT WISE TRANSACTION AMOUNT", 
                     height=1000,color_discrete_sequence=px.colors.sequential.Jet)

    st.plotly_chart(fig_bar_1)

    fig_bar_2=px.bar(tacyg,y="Districts", x="Transaction_count", orientation= "h", title=f" {state.upper()} STATE DISTRICT AND TRANSACTION COUNT", 
                     height=1000,color_discrete_sequence=px.colors.sequential.Magma_r)

    st.plotly_chart(fig_bar_2)


#Map_User

#Map_User_Plot_1

def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]

    muy.reset_index(drop=True,inplace=True)

    muyg=(muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum())

    muyg.reset_index(inplace=True) 

    fig_scatter_1= px.scatter(muyg, x= "States", y=["RegisteredUsers","AppOpens"], 
                            title=f"{year} REGISTERED USERS AND APP OPENS", width=800, height=800)

    st.plotly_chart(fig_scatter_1)

    return muy

#Map_User_Plot_2

def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]

    muyq.reset_index(drop=True,inplace=True)

    muyqg=(muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum())

    muyqg.reset_index(inplace=True) 

    fig_line_1= px.line(muyqg, x= "States", y=["RegisteredUsers","AppOpens"], 
                            title=f"{quarter} QUARTER REGISTERED USERS AND APP OPENS", width=800, height=800, markers=True)

    st.plotly_chart(fig_line_1)

    return muyq

#Map_User_Plot_3

def map_user_plot_3(df,states):

    muyqs=df[df["States"]== states]

    muyqs.reset_index(drop=True,inplace=True)

    fig_map_user_bar_1=px.bar(muyqs,y="RegisteredUsers", x="Districts", title=f" {states.upper()} REGISTERED USERS", height=600, 
                            color_discrete_sequence=px.colors.sequential.Darkmint)

    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2=px.bar(muyqs,y="AppOpens", x="Districts", title=f" {states.upper()} REGISTERED USERS", height=600, 
                            color_discrete_sequence=px.colors.sequential.Rainbow)

    st.plotly_chart(fig_map_user_bar_2)

#Top_Insurance_Plot_1

def Top_insur_plot_1(df,state):

    tiy=df[df["States"]==state]

    tiy.reset_index(drop=True,inplace=True)

    tiyg=(tiy.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum())

    tiyg.reset_index(inplace=True) 

    fig_top_insur_bar_1=px.bar(tiy,x="Quarter", y="Transaction_count",hover_data="Pincodes", title=f" {state.upper()} STATE TOP INSURANCE TRANSACTION COUNT", height=600, 
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_top_insur_bar_1)

    fig_top_insur_bar_2=px.bar(tiy,x="Quarter", y="Transaction_amount",hover_data="Pincodes", title=f" {state.upper()} STATE TOP INSURANCE TRANSACTION AMOUNT", height=600, 
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)

    st.plotly_chart(fig_top_insur_bar_2)


#Top_User_Plot_1

def top_user_plot_1(df,year):

    tuy=df[df["Years"]==year]

    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])[["RegisteredUsers"]].sum())

    tuyg.reset_index(inplace=True)      

    fig_top_plot_1 = px.bar( tuyg, x="States", y="RegisteredUsers", color="Quarter", width=800, height=800,
                        color_discrete_sequence=px.colors.sequential.Rainbow, title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#Top_User_Plot_2

def top_user_plot_2(df,state):

    tuys=df[df["States"]== state]

    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys, x="Quarter", y="RegisteredUsers", title=f" {state.upper()} STATE REGISTERED USERS AND PINCODES", width=800, height=800, color="RegisteredUsers",
                        hover_data="Pincodes", color_continuous_scale=px.colors.sequential.amp)

    st.plotly_chart(fig_top_plot_2)

    return tuys

#Top_Charts

def top_chat_transaction_count(table_name):

    mydb= psycopg2.connect(host="localhost",
                        user= 'postgres',
                        database="phonepe-dataset",
                        password="Aravind#123",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT_1

    query1= f'''SELECT states,SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                LIMIT 5'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "transaction_count"))

    fig_pie_1=px.pie(data_frame=df_1,names="states", values="transaction_count",width=600, title= "TRANSACTION COUNT", hole=0.5, hover_name="states")

    st.plotly_chart(fig_pie_1)

    #PLOT_2

    query2= f'''SELECT states,SUM(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count DESC
        LIMIT 5'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "transaction_count"))

    fig_pie_2=px.pie(data_frame=df_2,names="states", values="transaction_count",width=600, title= "TRANSACTION COUNT DESC", hole=0.5, hover_name="states")

    st.plotly_chart(fig_pie_2)

    #PLOT_3

    query3= f'''SELECT states,AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_line_3=px.line(data_frame=df_3,x="states", y="transaction_count",width=900,height=600, title= "TRANSACTION COUNT AVEG", hover_name="states", markers=True)

    st.plotly_chart(fig_line_3)

#Query7

def top_chart_brands(table_name,states):

    mydb= psycopg2.connect(host="localhost",
                        user= 'postgres',
                        database="phonepe-dataset",
                        password="Aravind#123",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT_1

    query1= f'''SELECT brands, SUM (transaction_count) AS transaction_count
                FROM {table_name}
                WHERE states= '{states}'
                GROUP BY brands'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("brands", "transaction_count"))

    fig_line_1=px.line(data_frame=df_1,x="brands", y="transaction_count",width=800, title= "TRANSACTION COUNT", hover_name="brands",
                       markers=True)

    st.plotly_chart(fig_line_1)

    #PLOT_2

    query2= f'''SELECT brands, AVG (transaction_count) AS transaction_count
                FROM {table_name}
                WHERE states= '{states}'
                GROUP BY brands'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("brands", "transaction_count"))

    fig_line_2=px.line(data_frame=df_2, x="brands", y="transaction_count",width=800, title= " AVEG TRANSACTION COUNT", hover_name="brands", markers=True)

    st.plotly_chart(fig_line_2)

#Queries8910

def top_chart_transaction_amount(table_name):

      mydb= psycopg2.connect(host="localhost",
                          user= 'postgres',
                          database="phonepe-dataset",
                          password="Aravind#123",
                          port="5432")
      cursor=mydb.cursor()

      #PLOT_1

      query1= f'''SELECT states,SUM(transaction_amount) AS transaction_amount
                  FROM aggregated_insurance
                  GROUP BY states
                  ORDER BY transaction_amount
                  LIMIT 10'''

      cursor.execute(query1)
      table_1=cursor.fetchall()
      mydb.commit()

      df_1=pd.DataFrame(table_1, columns=("states", "transaction_amount"))

      fig_bar_1=px.bar(data_frame=df_1,x="states", y="transaction_amount",color_discrete_sequence=px.colors.sequential.Rainbow,width=1000,height=600, 
                      title= "TRANSACTION AMOUNT", hover_name="states",
                    )

      st.plotly_chart(fig_bar_1)

      #PLOT_2

      query2= f'''SELECT states,MAX(transaction_amount) AS transaction_amount
                  FROM aggregated_insurance
                  GROUP BY states
                  ORDER BY transaction_amount'''

      cursor.execute(query2)
      table_2=cursor.fetchall()
      mydb.commit()

      df_2=pd.DataFrame(table_2, columns=("states", "transaction_amount"))

      fig_bar_2=px.bar(data_frame=df_2,x="states", y="transaction_amount",color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1000,height=600, 
                      title= "MAX TRANSACTION AMOUNT", hover_name="states",
                    )
      st.plotly_chart(fig_bar_2)

      #PLOT_3

      query3= f'''SELECT states,MIN(transaction_amount) AS transaction_amount
                  FROM aggregated_insurance
                  GROUP BY states
                  ORDER BY transaction_amount DESC'''

      cursor.execute(query3)
      table_3=cursor.fetchall()
      mydb.commit()

      df_3=pd.DataFrame(table_3, columns=("states", "transaction_amount"))

      fig_bar_3=px.bar(data_frame=df_3,x="states", y="transaction_amount",color_discrete_sequence=px.colors.sequential.Aggrnyl,width=1000,height=600, 
                      title= "MIN TRANSACTION AMOUNT", hover_name="states",
                    )

      st.plotly_chart(fig_bar_3)

#Queries1112

def total_transaction_amount_year(table_name):

    mydb= psycopg2.connect(host="localhost",
                        user= 'postgres',
                        database="phonepe-dataset",
                        password="Aravind#123",
                        port="5432")
    cursor=mydb.cursor()

    query1= f'''SELECT years, SUM(transaction_amount) AS transaction_amount
            FROM aggregated_insurance
            GROUP BY years'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("years", "transaction_amount"))

    fig_line_1=px.line(data_frame=df_1,x="years", y="transaction_amount",color_discrete_sequence=px.colors.sequential.Rainbow,width=800,height=600, 
                    title= "TRANSACTION AMOUNT", hover_name="years",markers=True
                )

    st.plotly_chart(fig_line_1)

#Streamlit

st.set_page_config(layout= "wide")

st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

  select= st.selectbox("Main Menu",["Home","DATA EXPLORATION","TOP CHARTS"])

  year=st.selectbox("Select the Year to know About US",["2016","2017","2018","2019","2020","2021","2022","2023"])

if select == "Home":
 


 if year == "2016":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2016.png"))

 if year == "2017":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2017.png"))

 if year == "2018":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2018.png"))

 if year == "2019":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2019.png"))

 if year == "2020":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2020.png"))

 if year == "2021":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2021.png"))

 if year == "2022":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2022.png"))

 if year == "2023":
    
    st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 2023.png"))

 

elif select =="DATA EXPLORATION":
   
   tab1,tab2,tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

   with tab1:
      
     method = st.radio("Select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

     if method == "Insurance Analysis":
        
        col1,col2=st.columns(2)
        with col1:
        
         years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].unique().max(),
                         Aggre_insurance["Years"].min())

        tac_Y=Transaction_amount_count_Y(Aggre_insurance, years)

        col1,col2=st.columns(2)
        with col1:

         quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].unique().max(),tac_Y["Quarter"].min())
        Transaction_amount_count_Y_Q(tac_Y,quarters)
     
     elif method == "Transaction Analysis":
        
        col1,col2=st.columns(2)
        with col1:
        
         years=st.slider("Select The Year_Tran",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].unique().max(),
                         Aggre_transaction["Years"].min())
         
        Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)

        col1,col2=st.columns(2)
        with col1:
             states=st.selectbox("SELECT THE STATE", Aggre_tran_tac_Y["States"].unique())

        Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)   

        col1,col2=st.columns(2)
        with col1:

         quarters=st.slider("Select The Quarter_Tran",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].unique().max(),Aggre_tran_tac_Y["Quarter"].min())
        Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)  

        col1,col2=st.columns(2)
        with col1:
             states=st.selectbox("SELECT THE STATE FROM",Aggre_tran_tac_Y_Q["States"].unique())

        Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)   

     
     elif method == "User Analysis":
        
        col1,col2=st.columns(2)
        with col1: 
        
         years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].unique().max(),
                         Aggre_user["Years"].min())
         
        Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

        col1,col2=st.columns(2)
        with col1:

         quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].unique().max(),Aggre_user_Y["Quarter"].min())
        Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters) 

        col1,col2=st.columns(2)
        with col1:
             states=st.selectbox("SELECT THE STATE", Aggre_user_Y_Q["States"].unique())

        Agrre_user_plot_3(Aggre_user_Y_Q,states)   

   with tab2:
      method_2=st.radio("Select the Method",["Map Insurance", "Map Transaction","Map User"])

      if method_2== "Map Insurance":
         
         col1,col2=st.columns(2)
         with col1:
         
            years=st.slider("Select The Year_Map_I",map_insurance["Years"].min(),map_insurance["Years"].unique().max(),
                          map_insurance["Years"].min())
            
         map_insur_tac_Y=Transaction_amount_count_Y(map_insurance,years)

         col1,col2=st.columns(2)
         with col1:
             states=st.selectbox("MAP INSURANCE_SELECT THE STATE",  map_insur_tac_Y["States"].unique())

         Map_Insur_District(map_insur_tac_Y,states)  

         col1,col2=st.columns(2)
         with col1:

          quarters=st.slider("Select The Quarter_Map_I",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].unique().max(),
                             map_insur_tac_Y["Quarter"].min())
         map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)  

         col1,col2=st.columns(2)
         with col1:
               states=st.selectbox("SELECT THE STATE_MAP_I",map_insur_tac_Y_Q["States"].unique())

         Map_Insur_District(map_insur_tac_Y_Q,states)   


      if method_2== "Map Transaction":
         
         col1,col2=st.columns(2)
         with col1:
         
            years=st.slider("Select The Year_Map_T",map_transaction["Years"].min(),map_transaction["Years"].unique().max(),
                         map_transaction["Years"].min())
            
         map_tran_tac_Y=Transaction_amount_count_Y(map_transaction,years)

         col1,col2=st.columns(2)
         with col1:
             states=st.selectbox("MAP TRANSACTION_SELECT THE STATE", map_tran_tac_Y["States"].unique())

         Map_Insur_District(map_tran_tac_Y,states)  

         col1,col2=st.columns(2)
         with col1:

          quarters=st.slider("Select The Quarter_Map_T",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].unique().max(),
                            map_tran_tac_Y["Quarter"].min())
         map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)  

         col1,col2=st.columns(2)
         with col1:
               states=st.selectbox("SELECT THE STATE_MAP_T",map_tran_tac_Y_Q["States"].unique())

         Map_Insur_District(map_tran_tac_Y_Q,states)   
         col1,col2=st.columns(2)
        

      
      if method_2== "Map User":
         
         col1,col2=st.columns(2)
         with col1:
         
            years=st.slider("Select The Year_Map_U",map_user["Years"].min(),map_user["Years"].unique().max(),
                        map_user["Years"].min())
            
         map_user_Y=map_user_plot_1(map_user,years)

         col1,col2=st.columns(2)
         with col1:

          quarters=st.slider("Select The Quarter_Map_U",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].unique().max(),
                           map_user_Y["Quarter"].min())
         map_user_Y_Q=map_user_plot_2(map_user_Y, quarters)  

         col1,col2=st.columns(2)
         with col1:
               states=st.selectbox("SELECT THE STATE_MAP_S",map_user_Y_Q["States"].unique())

         map_user_plot_3(map_user_Y_Q,states)   
         

   with tab3:
      method_3=st.radio("Select the Method",["Top Insurance", "Top Transaction","Top User"])

      if method_3== "Top Insurance":
        
        col1,col2=st.columns(2)
        with col1:
         
            years=st.slider("Select The Year_Top_I",top_insurance["Years"].min(),top_insurance["Years"].unique().max(),
                          top_insurance["Years"].min())
            
        top_insur_tac_Y=Transaction_amount_count_Y(top_insurance,years)

        col1,col2=st.columns(2)
        with col1:
               states=st.selectbox("SELECT THE STATE_TOP_S",top_insur_tac_Y["States"].unique())

        Top_insur_plot_1(top_insur_tac_Y,states)  


        col1,col2=st.columns(2)
        with col1:

          quarters=st.slider("Select The Quarter_Top_IQ",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].unique().max(),
                           top_insur_tac_Y["Quarter"].min())
        top_insur_tac_Y_Q =Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)  
  
      
      if method_3== "Top Transaction":
       
        col1,col2=st.columns(2)
        with col1:
          
            years=st.slider("Select The Year_Top_T",top_transaction["Years"].min(),top_transaction["Years"].unique().max(),
                          top_transaction["Years"].min())
            
        Top_tran_tac_Y=Transaction_amount_count_Y(top_transaction,years)

        col1,col2=st.columns(2)
        with col1:
                states=st.selectbox("SELECT THE STATE_TOP_TS",Top_tran_tac_Y["States"].unique())

        Top_insur_plot_1(Top_tran_tac_Y,states)  


        col1,col2=st.columns(2)
        with col1:

          quarters=st.slider("Select The Quarter_Top_TQ",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].unique().max(),
                            Top_tran_tac_Y["Quarter"].min())
          Top_tran_tac_Y_Q =Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)  
         
      
      if method_3== "Top User":
         
        col1,col2=st.columns(2)
        with col1:
        
          years=st.slider("Select The Year_Top_UY",top_user["Years"].min(),top_user["Years"].unique().max(),
                        top_user["Years"].min())
          
      Top_user_Y=top_user_plot_1(top_user,years)

      col1,col2=st.columns(2)
      with col1:
              states=st.selectbox("SELECT THE STATE_TOP_TU",Top_user_Y["States"].unique())

      top_user_plot_2(Top_user_Y,states)  


elif select== "TOP CHARTS":
     
    question= st.selectbox("Choose your Question",["1.Top Five Transaction Count in Aggregated Insurance",
                                                  "2.Top Five Transaction Count in Aggregated Transaction",
                                                  "3.Top Five Transaction Count in Top Insurance",
                                                  "4.Top Five Transaction Count in Map Insurance",
                                                  "5.Top Five Transaction Count in Map Transaction",
                                                  "6.Top Five Transaction Count in Top Transaction",
                                                  "7.Brand wise Transaction Count in Aggregated User",
                                                  "8.Top ten,Max,and Min Transaction amount in Aggregated Insurance",
                                                  "9.Top ten,Max,and Min Transaction amount in Map Insurance",
                                                  "10.Top ten,Max,and Min Transaction amount in Top Insurance",
                                                  "11.Year wise total Transaction Amount in Aggregated insurance",
                                                  "12.Year wise total Transaction Amount in Map insurance"])


    if  question == "1.Top Five Transaction Count in Aggregated Insurance":
        
        top_chat_transaction_count("aggregated_insurance")

    elif question == "2.Top Five Transaction Count in Aggregated Transaction":
      
        top_chat_transaction_count("aggregated_transaction")

    elif question == "3.Top Five Transaction Count in Top Insurance":
      
        top_chat_transaction_count("top_insurance")

    elif question == "4.Top Five Transaction Count in Map Insurance":
      
        top_chat_transaction_count("map_insurance")

    elif question ==  "5.Top Five Transaction Count in Map Transaction":
      
        top_chat_transaction_count("map_transaction")

    elif question == "6.Top Five Transaction Count in Top Transaction":
      
        top_chat_transaction_count("top_transaction")

    elif question == "7.Brand wise Transaction Count in Aggregated User":
        
        states= st.selectbox("Choose the State",Aggre_user["States"].unique())
        
        top_chart_brands("aggregated_user",states)

    elif question == "8.Top ten,Max,and Min Transaction amount in Aggregated Insurance":
      
        top_chart_transaction_amount("aggregated_insurance")

    elif question == "9.Top ten,Max,and Min Transaction amount in Map Insurance":
      
        top_chart_transaction_amount("map_insurance")

    elif question == "10.Top ten,Max,and Min Transaction amount in Top Insurance":
      
        top_chart_transaction_amount("top_transaction")

    elif question == "11.Year wise total Transaction Amount in Aggregated insurance":
        
        total_transaction_amount_year("aggregated_insurance")

    elif question == "12.Year wise total Transaction Amount in Map insurance":
        
        total_transaction_amount_year("map_insurance")

with st.sidebar:

 st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 01.png"))
 
 st.image(Image.open(r"C:\Users\Aravind Chirshtopher\OneDrive\Desktop\Phonepe since 2016\pp 02.png"))