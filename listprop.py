import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

APP_TITTLE='Listed properties up to 600$ pw'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
  
def main():
    st.set_page_config(APP_TITTLE,layout='centered',page_icon="https://cdn5.ep.dynamics.net/__resources/img/favicon-2017.d516ca4620c34215af43404a41b460ed.ico")
    st.title(APP_TITTLE) 
    #hide the menu, adjusting the padding-top margin
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    .block-container {
                    padding-top: 2rem;
                }
    .css-1oe5cao {
                    padding-top: 2.5rem;
    }
    </style>
    """
    st.markdown(hide_streamlit_style,unsafe_allow_html=True)
    dict1 = {'RayWhite Epping':'https://raywhiteepping.com.au',
               'RayWhite Ryde':'https://raywhiteryde.com.au',
               'RayWhite Eastwood':'https://raywhiteeastwood.com.au',
               'RayWhite North Ryde':'https://raywhitenorthryde.com.au',
               'RayWhite Meadowbank':'https://raywhitemeadowbank.com.au',
               'RayWhite Carlingford':'https://raywhitecarlingford.com.au',
               'RayWhite Ashfield':'https://raywhiteashfield.com.au',
               'RayWhite Summer Hill':'https://raywhitesummerhill.com.au',
               'RayWhite Paramatta':'https://raywhiteparramatta.com.au'
              
              }
 
    listing = st.multiselect('',['All RayWhite suburbs']+list(dict1.keys()))
    
    dict2 = dict1
    
    if listing:
        if 'All RayWhite suburbs' not in listing:
            dict2 = {}
            for i in listing:
                if i in list(dict1.keys()):
                    dict2[i] = dict1[i]
       
    for suburb in dict2:
        url = dict2[suburb] + '/properties/residential-for-rent?category=&keywords=&minBaths=0&minBeds=2&minCars=0&rentPrice=0-31284&sort=updatedAt+desc&suburbPostCode='
        page = requests.get(url, headers=headers)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content,'html.parser')
            proplist = soup.find_all('li',{'class':'proplist_item_wrap'})
            for prop in proplist:
                description = prop.find('span',{'class':'proplist_item_descriptor muted'}).text
                price = prop.find('span',{'class':'proplist_item_price'}).text
                address = prop.find('h2',{'class':'gamma'}).find('a')['data-ev-label']
                link = dict2[suburb] + prop.find('a')['href']
                image = prop.find('div',{'class':'proplist_item_image'}).find('img')['src']
                
                #print(url)
                bed = prop.find('li',{'class':'bed'}).text
                bath = prop.find('li',{'class':'bath'}).text
                #car = prop.find('li',{'class':'car'}).text
                       
                col1,col2 = st.columns(2)
                
                with col1:
                    st.image(image)
                with col2:
                    st.markdown('**'+address+'**')
                    st.markdown(description+' - '+bed+', '+bath)
                    st.markdown(price)
                    st.markdown(link)
                
                #get the property details
                #page_prop = requests.get(link, headers = headers)
                #time.sleep(1)
                #soup_prop = BeautifulSoup(page_prop.content,'html.parser')
                #agent = soup_prop.find('div',{'class':'pdp_agents'})
                #print(link)
                #print(agent)
                 
                #creating dataframe - currently not used       
                #dict_prop = {'Suburb':suburb,'Address':address,'Description':description,'Price':price,'Link':link}
                #list_prop.append(dict_prop)     

    #df = pd.DataFrame(list_prop)  
    #st.dataframe(df,use_container_width=True, width=1000)           
                

if __name__=='__main__':
    main()