import pandas as pd
import streamlit as st
import os
import tempfile
from Analyzer import Column, analyze
from io import BytesIO
import requests

#FUNCTION ---------------------------------------------------------------------------------------------
@st.cache_data
def get_data(input, type = '', encode = None):
    try:
        try:
            if type == 'upload':
                data = pd.read_csv(input, encoding = encode)
            elif type == 'link':
                file_id = input.split('/')[-2]
                link = f"https://drive.google.com/uc?id={file_id}"
                data = pd.read_csv(link, encoding = encode)
            
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, 'data.csv')
            data.to_csv(temp_path, index = False)
        except:
            data, temp_path = None, None
    except:
        print('Data have not uploaded yet')
    return data, temp_path


def show_data(result):
    for i, v in result.all_data.items():
        with st.expander(f'Data of {i}'):
            try:
                st.dataframe(v)
            except:
                st.metric(label = i, value = v)


#WEBAPP ---------------------------------------------------------------------------------------------


st.set_page_config(
    page_title="Marketing Auto Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.subheader('AUTHOR')
    image_url = "https://drive.google.com/uc?id=1f8jbbkrSyn4OfglO0PS9uv8DbVqEQQfv"
    response = requests.get(image_url)
    img_data = BytesIO(response.content)
    st.image(img_data, width = 150)
    st.markdown('👨‍💻 Hoàng Hảo')
    st.markdown('🏠 Ho Chi Minh City')
    st.markdown('📞 Phone: 0866 131 594')
    st.markdown('✉️ hahoanghao1009@gmail.com')
    st.write()
    st.write()
    i1, i2, i3 = st.columns(3)
    with i1:
        image_url = 'https://cdn-icons-png.flaticon.com/256/174/174857.png'
        linkedin_url = 'https://www.linkedin.com/in/hahoanghao1009/'

        clickable_image_html = f"""
            <a href="{linkedin_url}" target="_blank">
                <img src="{image_url}" alt="Clickable Image" width="50">
            </a>
        """
        st.markdown(clickable_image_html, unsafe_allow_html=True)

    with i2:
        image_url = 'https://cdn-icons-png.flaticon.com/512/25/25231.png'
        git_url = 'https://github.com/HoangHao1009/'

        clickable_image_html = f"""
            <a href="{git_url}" target="_blank">
                <img src="{image_url}" alt="Clickable Image" width="50">
            </a>
        """
        st.markdown(clickable_image_html, unsafe_allow_html=True)
    with i3:
        image_url = 'https://cdn-icons-png.flaticon.com/512/3536/3536394.png'
        fb_url = 'https://www.facebook.com/hoanghao1009/'

        clickable_image_html = f"""
            <a href="{fb_url}" target="_blank">
                <img src="{image_url}" alt="Clickable Image" width="50">
            </a>
        """
        st.markdown(clickable_image_html, unsafe_allow_html=True)
    st.divider()



st.title('MARKETING AUTO ANALYZER TOOL',
         anchor = 'Marketing title')

if 'analysis_chose' not in st.session_state.keys():
    st.session_state['analysis_chose'] = None

if 'predictor' not in st.session_state.keys():
    st.session_state['predictor'] = None

if 'predict_data' not in st.session_state.keys():
    st.session_state['predict_data'] = None


with st.expander(label = 'UPLOAD DATA HERE'):
    data = None
    upload = st.columns([0.1, 0.45, 0.45])
    with upload[0]:
        encode = st.selectbox('Encoding type', options = ['utf-8', 'ISO-8859-1' , 'UTF-16'])
    with upload[1]:
        try:
            file_path = st.text_input('If data > 200 MB', placeholder = 'Put drive share link here')
            if file_path:
                data, temp_path = get_data(file_path, type = 'link', encode = encode)
        except:
            raise ValueError('LOAD FILE FAILED')
    with upload[2]:
        try:
            csv_data = st.file_uploader('If data < 200 MB', type = ['csv'])
            if csv_data:
                data, temp_path = get_data(csv_data, type = 'upload', encode = encode)
        except:
            raise ValueError('LOAD FILE FAILED')
    #use sample data
    use_sample = st.checkbox('Click if you want to use sample data', key = 'use_sample')
    if use_sample:
        data = pd.read_csv('sample_data/data.csv', encoding = encode)

    if data is not None:
        sale_chose, customer_chose = st.columns([0.25, 0.75])
        with sale_chose:
            with st.container(border = True):
                st.subheader('Sale Column')
                st.info('Please chose Sale Column')
                sale_col = st.selectbox(label = 'Please chose', options = [None] + data.columns.tolist(), key = 'sale',
                                        help = 'Chose [Sales] if you are using sample data')
        with customer_chose:
            with st.container(border = True):
                st.subheader('Customer Column')
                customer, customer_segment, segment_chose = st.columns(3)
                with customer:
                    st.info('Please chose Customer Column')
                    customer_col = st.selectbox(label = 'Please chose', options = [None] + data.columns.tolist(), key = 'customer',
                                                help = 'Chose [Customer ID]/ [Customer Name] if you are using sample data')
                with customer_segment:
                    st.info('Please chose Segment Column')
                    segment_col = st.selectbox(label = 'Please chose', options = [None] + data.columns.tolist(), key = 'segment',
                                               help = 'Chose any segment column you want')
                with segment_chose:
                    st.info('Please chose Segment for Customer')
                    if segment_col:
                        chose_col = st.multiselect(label = 'Please chose', options = ['All'] + data[segment_col].unique().tolist(),
                                                   help = 'Chose which segment in segment column')
                        if 'All' in chose_col:
                            chose_col = data[segment_col].unique().tolist()
                    else:
                        st.write('You have not chose Customer Segment')
        with st.container(border = True):
            st.subheader('Date Column')
            date, date_format_chose, year_chose, month_chose, day_chose = st.columns(5)
            with date:
                st.info('Please chose Date Column')
                date_col = st.selectbox(label = 'Please chose', options = [None] + data.columns.tolist(), key = 'date',
                                        help = 'Chose [Order Date] if you are using sample data')
            with date_format_chose:
                st.info('Please specify Date-time format')
                date_format = st.text_input(label = 'Please type', help = 'Type %d/%m/%Y if you are using sample data', 
                                            placeholder = '%d/%m/%Y')
            try:
                to_date = pd.to_datetime(data[date_col], format = date_format)
            except:
                st.write('Your chosen seem not to be exactly')
                to_date = None
            with year_chose:
                st.info('Please select year')
                if to_date is not None:
                    years = st.multiselect(label = 'Please chose', 
                                   options = ['All'] + to_date.dt.year.unique().tolist(),
                                   default = 'All')
                    if 'All' in years:
                        years = to_date.dt.year.unique().tolist()
                else:
                    st.write('You have not specify Date column')
            with month_chose:
                st.info('Please select month')
                if to_date is not None:
                    months = st.multiselect(label = 'Please chose', 
                                   options = ['All'] + to_date.dt.month.unique().tolist(),
                                   default = 'All')
                    if 'All' in months:
                        months = to_date.dt.month.unique().tolist()
                else:
                    st.write('You have not specify Date column')
            with day_chose:
                st.info('Please select day')
                if to_date is not None:
                    days = st.multiselect(label = 'Please chose', options = ['All'] + to_date.dt.day.unique().tolist(),
                                   default = 'All')
                    if 'All' in days:
                        days = to_date.dt.day.unique().tolist()
                else:
                    st.write('You have not specify Date column')

        with st.container(border = True):
            st.subheader('Your chosen data')
            try:
                customer = Column.mainColunm(
                    data[customer_col], data[segment_col], chose_col, type = 'customer'
                )
                sale = Column.Sale(data[sale_col])
                date = Column.Date(data[date_col], date_format = date_format,
                                year_chose = years, month_chose = months, day_chose = days)

                basicinfo = analyze.BasicInfo(customer, sale, date)
                st.dataframe(basicinfo.input)
            except:
                st.write('Please chosen data')

try:
    analyzer = analyze.AllAnalyze(customer, sale, date)
except:
    analyzer = None



analysis_type, results = st.columns([0.2, 0.8])
with analysis_type:
    with st.container(border = True):
        st.subheader('ANALYSIS')
        for i in ['Basic Info', 'Growth', 'NewExisting', 'Retention', 'Cohort', 'Segmentation']:
            x = st.form(key = i, border = False)
            with x:
                submit_button = st.form_submit_button(label = i)
                if submit_button:
                    st.session_state['analysis_chose'] = x._form_data[0]
        st.divider()
        st.subheader('PREDICT')
        y = st.form(key = 'Life Time Value Predictor', border = False)
        with y:
            submit_button = st.form_submit_button(label = 'Life Time Value Predictor')
            if submit_button:
                st.session_state['analysis_chose'] = y._form_data[0]

with results:
    st.info(f"ANALYSIS CHOSING: ➡️ {st.session_state['analysis_chose']}",
            icon = '⚙️')

    if st.session_state['analysis_chose'] == 'Basic Info':
        result = analyzer.basicinfo
        show_data(result)
        basicinfo1 = st.columns(3)
        with basicinfo1[0]:
            st.info('Total Revenue')
            st.metric(label='', value=f"{round(result.all_data['total_revenue']):,}")
        with basicinfo1[1]:
            st.info('Unique Customer')
            st.metric(label = '', value = round(result.all_data['unique_customer']))
        with basicinfo1[2]:
            st.info('Average Customer Revenue')
            st.metric(label = '', value = f"{round(result.all_data['avg_customer_revenue']):,}")
        basicinfo2 = st.columns(2)
        with basicinfo2[0]:
            st.plotly_chart(result.all_px['segment_revenue_px'], use_container_width = True)
        with basicinfo2[1]:
            st.plotly_chart(result.all_px['segment_unique_customer_px'], use_container_width = True)
        st.plotly_chart(result.all_px['customer_revenue_px'], use_container_width = True)

    elif st.session_state['analysis_chose'] == 'Growth':
        result = analyzer.growth
        show_data(result)
        growth1 = st.columns(2)
        with growth1[0]:
            st.plotly_chart(result.all_px['monthly_revenue_px'], use_container_width = True)
            st.plotly_chart(result.all_px['monthly_unique_customer_px'], use_container_width = True)
        with growth1[1]:
            st.plotly_chart(result.all_px['segment_monthly_revenue_px'], use_container_width = True)
            st.plotly_chart(result.all_px['segment_monthly_customer_px'], use_container_width = True)
            
    elif st.session_state['analysis_chose'] == 'NewExisting':
        result = analyzer.newexisting
        show_data(result)
        ne = st.columns(2)
        with ne[0]:
            st.plotly_chart(result.all_px['count_px'], use_container_width = True)
            st.plotly_chart(result.all_px['month_new_percent_px'], use_container_width = True)

        with ne[1]:
            st.plotly_chart(result.all_px['type_percent_px'], use_container_width = True)
            st.plotly_chart(result.all_px['segment_monthly_new_percent_px'], use_container_width = True)
        st.plotly_chart(result.all_px['segment_count_px'], use_container_width = True)
        
    elif st.session_state['analysis_chose'] == 'Retention':
        result = analyzer.retention
        show_data(result)
        retention = st.columns(2)
        with retention[0]:
            st.plotly_chart(result.all_px['retention_px'], use_container_width = True)
        with retention[1]:
            st.plotly_chart(result.all_px['retention_pct_px'], use_container_width = True)
    elif st.session_state['analysis_chose'] == 'Cohort':
        result = analyzer.cohort
        show_data(result)
        cohort = st.columns(2)
        with cohort[0]:
            st.plotly_chart(result.all_px['by_revenue_px'], use_container_width = True)
            st.plotly_chart(result.all_px['by_revenue_pct_px'], use_container_width = True)
        with cohort[1]:
            st.plotly_chart(result.all_px['by_retention_px'], use_container_width = True)
            st.plotly_chart(result.all_px['by_retention_pct_px'], use_container_width = True)
    elif st.session_state['analysis_chose'] == 'Segmentation':
        result = analyzer.segmentation
        show_data(result)
        seg = st.columns(3)
        with seg[0]:
            st.plotly_chart(result.all_px['recency_px'], use_container_width = True)
            st.plotly_chart(result.all_px['recency_frequency_px'], use_container_width = True)
        with seg[1]:
            st.plotly_chart(result.all_px['frequency_px'], use_container_width = True)
            st.plotly_chart(result.all_px['recency_monetary_px'], use_container_width = True)
        with seg[2]:
            st.plotly_chart(result.all_px['monetary_px'], use_container_width = True)
            st.plotly_chart(result.all_px['frequency_monetary_px'], use_container_width = True)
    elif st.session_state['analysis_chose'] == 'Life Time Value Predictor':
        predictor = analyzer.predictor
        hint_px = predictor.cluster_hint()
        with st.expander('Click here if you want to hint about cluster'):
            st.plotly_chart(hint_px)
            st.info('Data using to predict LTV cluster')
            st.dataframe(predictor.df)
        set_params = st.columns(5)
        with set_params[0]:
            revenue_clusters = st.number_input('Set Customer LTV Cluster',
                                                help = 'You can chose based on cluster hint',
                                                value = 4)
        with set_params[1]:
            remove_outlier_quantile = st.number_input('Set quantile of outlier',
                                                        min_value = 0.0,
                                                        max_value = 1.0,
                                                        step = 0.01,
                                                        value = 1.0,
                                                        help = 'Remove outlier out of quantile you set')
        with set_params[2]:
            cv = st.number_input('Set cv for chosing algorithm', value = 5)
        with set_params[3]:
            use_rs = st.checkbox('Click if you want to use Random Search', value = True)
        with set_params[4]:
            use_mm = st.checkbox('Click if you want to use only modern model', value = True)

        run = st.button('Run chosing best predictor')
        if run:
            with st.spinner('Running algorithm, please wait'):
                predictor.chose_best_predictor(revenue_clusters, remove_outlier_quantile, cv,
                                            use_rs, use_mm)
            st.session_state['predictor'] = predictor
        try:
            st.subheader(f"Best predictor for your data is [{str(st.session_state['predictor'].best_estimator)}]")
            best_model, ltv_info = st.columns(2)
            with best_model:
                with st.expander('Click to see predictor scores'):
                    st.dataframe(predictor.predictor_scores.drop(['best_estimator'], axis = 1))
            with ltv_info:
                with st.expander('Click to see LTV cluster info'):
                    st.dataframe(predictor.ltv_cluster_info)
        except:
            pass

        st.subheader(f'Using your best predictor')
        predict_data = st.file_uploader('Upload data you want to predict',
                                        help = 'Same type with data you have uploaded')
        if predict_data:
            st.session_state['predict_data'] = predict_data
        if st.session_state['predict_data'] is not None:
            predict_data = pd.read_csv(st.session_state['predict_data'])
            predictor = st.session_state['predictor']
            p_customer = Column.mainColunm(
                predict_data[customer_col], predict_data[segment_col], chose_col, type = 'customer'
            )
            p_sale = Column.Sale(predict_data[sale_col])
            p_date = Column.Date(predict_data[date_col], date_format = date_format,
                            year_chose = years, month_chose = months, day_chose = days)
            rfm_p = analyze.RFMSegmentaion(p_customer, p_sale, p_date)
            predict = st.button('Predict')
            if predict:
                ltv_predict = predictor.run_best_predictor(rfm_p)
                result = pd.merge(ltv_predict, predictor.ltv_cluster_info[['LTV Cluster', 'Life Time Value (Revenue)']],
                                  how = 'left', left_on = 'Life Time Value Predicted', right_on = 'LTV Cluster')
                st.dataframe(result.drop(['Life Time Value Predicted', 'LTV Cluster'], axis = 1))
            else:
                pass
