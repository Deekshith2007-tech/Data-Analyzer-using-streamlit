import streamlit as st
import pandas as pd
from io import BytesIO
import time
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Data Analyzer',page_icon=':joy:')
st.sidebar.title('Data analyzer')
file=st.file_uploader("upload file",type=['csv','xlsx'],width=400)
menu=st.sidebar.radio('Sections:',options=['data preview','Data summary','Missing Data','Visualize data'])

if file is not None:
    file_type=file.name.split(".")[-1]
    if file_type=='csv':
        data=pd.read_csv(file)
    elif file_type=='xlsx':
        data=pd.read_excel(file)
    else:
        st.error("sorry!unsupport file")
    data.index=range(1,len(data)+1)
    data.index.name='S.no'


#=========================================DATA PREVIEW=============================#
    if menu=='data preview':
        st.title(f'{menu}')
        st.success('File Uploaded Successfully')
        st.write('### File Name:',file.name)
        st.dataframe(data)
        st.write('Data Size',data.size)
        st.write('No.of.rows',data.shape[0])
#===========================================DATA SUMMARY===========================#
    if menu=='Data summary':
        st.title(f'Data Summary')
        st.write('Data Size',data.size)
        st.write('No.of.rows',data.shape[0])
        st.write('No.of.Columns',data.shape[1])
        st.write('Data Shape:',data.shape)
        dtype=pd.DataFrame({"columns:":list(data.columns),"data types:":list(data.dtypes)})
        dtype.index=range(1,len(dtype)+1)
        dtype.index.name="S.no"
        dtype.to_html(index=False,justify="center")
        st.dataframe(dtype,width=550)
#=========================================MISSING DATA==============================#
    if menu=='Missing Data':
        st.title(f"{menu}")
        st.write('### Missing Values:')
        missing_count=pd.DataFrame({'columns':data.columns,'count':list(data.isnull().sum())})
        missing_count.index=range(1,len(missing_count)+1)
        missing_count.index.name='S.no'
        st.dataframe(missing_count)
        st.write('### Total Missing value in dataset:',missing_count["count"].sum())
        st.write('### Percentage of Missing column')
        percentage=pd.DataFrame({'column':data.columns,'percentage':missing_count['count']/data.shape[0]*100})
        st.dataframe(percentage)
        st.header('cleaning Process')
        if st.button("Drop Missing Data"):
            st.warning("warning:Dropped to the Many rows reduce data quality")
            data.dropna(axis=0,inplace=True)
            st.success('Success! Missing value Dropped successfully')
            st.write('Cleaned Dataset:')
            st.dataframe(data)
            drop_data=data.to_csv(index=False).encode('utf-8')
            st.download_button('Download',data=drop_data,mime='text/csv')
#=======================================VISUALIZE DATA=============================#
    if menu=='Visualize data':
        st.title(f'{menu}')
        type=st.selectbox('File mode:',['original','missed values'],width=350)
        if type=='original':
            data=data
        st.dataframe(data,width=550,height=250)
        if type=='missed values':
            data.dropna(axis=0,inplace=True)
        plot=st.selectbox('Select plot type:',['none','scatter','histogram','line','bar','heat map'],width=350)
        columns=data.columns.to_list()
        if plot!='none':
            fig, a=plt.subplots()
            if plot=='heat map':
                st.header('Heat map')
                corr=data.corr(numeric_only=True)
                sns.heatmap(corr,annot=True,cmap='coolwarm')


            elif plot=='histogram':
                st.header(f'{plot} Plot:')
                x=st.selectbox('X axis',columns,width=300)
                plt.xlabel(x)
                bins=int(st.number_input('Enter the number of bins',max_value=20,value=6,width=300))
                color=st.color_picker('Graph colour',width=300,value='#1DB0D6')
                sns.histplot(data[x],bins=bins,color=color)
            else:
                x=st.selectbox('X axis:',columns,width=300)
                plt.xlabel(x)
                y=st.selectbox('Y axis',columns,width=300)
                plt.ylabel(y)
                color=st.color_picker('Graph colour',width=300,value='#1DB0D6')

            if plot=='scatter':
                st.header(f'{plot} Plot:')
                sns.scatterplot(data=data,x=data[x],y=data[y],color=color)
            if plot=='line':
                st.header(f'{plot} Plot:')
                sns.lineplot(data=data,x=x,y=y,color=color) 

            if plot=='bar':
                st.header(f'{plot} Plot:')
                sns.barplot(data=data,x=x,y=y,color=color)
                


        with st.spinner('Visualizing Data...'):
            time.sleep(0.5)
            plt.style.use('default')
            chart=st.pyplot(fig,width=500)
            buf=BytesIO()
            fig.savefig(buf,format='png')
            st.download_button('Download Image',data=buf.getvalue(),mime='image/png',file_name='chart.png')



    else:
        st.title('Data Analyzer')
        st.header('Analyze,clena and visualize your data in simple steps')
        st.subheader('Start Exploring your data now!')
        st.error('Upload a file to get started')