import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import datetime

df = pd.read_csv('data/PRECANDIDATOS.csv')

####################### LIMPIEZA Y ORDEN DEL DATAFRAME ####################### 

df2023 = df.copy()

####################### CONFIGURACION DE LA PÁGINA PRINCIPAL ####################### 

st.set_page_config(page_title = 'Elecciones 2023 - Sitio de consulta',
                    layout='wide',
                    initial_sidebar_state='collapsed')

st.markdown("<h1 style='text-align: center;'>Precandidatos de las elecciones PASO 2023</h1>", unsafe_allow_html=True)

tab_titles = [
                "Búsqueda de candidato",
                "Edad y género de los candidatos",
]
#tabs = st.tabs(tab_titles)

#df2023.loc[df2023['Cargo'] == 'PRESIDENTE Y VICEPRESIDENTE', 'Distrito'] = 'NACION'

#tabs = st.tabs(tab_titles)
#with tabs[0]:

madre4, madre5, madre6 = st.columns([0.15,0.7,0.15])

with madre5:

    st.markdown("<h2 style='text-align: center;'>Búsqueda de precandidatos</h2><br><br>", unsafe_allow_html=True)
    c4, c5, c6= st.columns(3)
    ######################################
    ####################### DROPDOWNS DE LA PRIMERA OPCION ####################### 


    with c4: 
        cargo = st.selectbox("Seleccione el cargo:",
                                            df2023['Cargo'].unique()
                                            )
        df_cargo = df2023.query('Cargo == @cargo')

    with c5: 
        agrupacion = st.multiselect("Seleccione la agrupación política:",
                                            df_cargo['AP'].unique(), ['UNION POR LA PATRIA', 'JUNTOS POR EL CAMBIO']
                                            )
        all_options = st.checkbox("Seleccionar todas las agrupaciones políticas")

        if all_options:
            agrupacion = df_cargo['AP']
        df_agrupacion = df_cargo.query('AP == @agrupacion')

    with c6: 
        distrito = st.selectbox("Seleccione distrito:",
                                            df_agrupacion['Distrito'].unique()
                                            )
        df_distrito = df_agrupacion.query("Distrito == @distrito")

    if 'PRESIDENTE Y VICEPRESIDENTE' in cargo:
                df_presi2 = df_distrito[['AP', 'Nombre_lista',
                'Subcategoria Cargo', 'Precandidatura']]
                st.dataframe(df_presi2, hide_index=True, use_container_width=True)
                @st.cache_data
                def convert_df(df_presi2):
                    return df_presi2.to_csv(index=False).encode('utf-8')
                
                csv = convert_df(df_presi2)

                st.download_button(
                "Descargar tabla como archivo CSV",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
                )
    else:
            df_resto2 = df_distrito[['AP', 'Nombre_lista', 'Distrito',
                'Subcategoria Cargo', 'Posicion','Precandidatura']]
            st.dataframe(df_resto2, hide_index=True, use_container_width=True)  
            @st.cache_data
            def convert_df(df_resto2):
                return df_resto2.to_csv(index=False).encode('utf-8')
                
            csv = convert_df(df_resto2)

            st.download_button(
                "Descargar tabla como archivo CSV",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
                )


    st.markdown("<h2 style='text-align: center;'><br>Distribución por edad y/o género de los precandidatos<br><br></h2>", unsafe_allow_html=True)
    c1, c2, c3,c7= st.columns(4)

    df2023_v2 = df2023
    num_bins=10
    bin_width = (df2023_v2['Edad'].max() - df2023_v2['Edad'].min()) / num_bins
    bin_edges = [df2023_v2['Edad'].min() + i * bin_width for i in range(num_bins + 1)]
    df2023_v2['Age_Bin'] = pd.cut(df2023_v2['Edad'], bins=bin_edges, labels=False)

    df2023_v2.loc[df2023_v2['Precandidatura'] == 'ADRIANA ELIZABETH REINOSO', 'Age_Bin'] = 1
    df2023_v2.loc[df2023_v2['Precandidatura'] == 'REINA XIOMARA IBAÑEZ', 'Age_Bin'] = 1
    df2023_v2.loc[df2023_v2['Precandidatura'] == 'OLGA VANESA PAOLA LEIVA', 'Age_Bin'] = 1
    df2023_v2['Age_Bin'] = df2023_v2['Age_Bin'].astype('int8')
    df2023_v2['Age_Range'] = df2023_v2['Age_Bin'].apply(lambda bin_label: f'{bin_edges[bin_label]:.0f}-{bin_edges[bin_label + 1]:.0f}')

    with c1:
        cargos = st.selectbox("Seleccionar cargo:",
                                                df2023_v2['Cargo'].unique()
                                                )
        df_cargos = df2023_v2.query('Cargo == @cargos')
    with c2:
        agrupaciones = st.selectbox("Seleccionar la agrupación política:",
                                            df_cargos['AP'].unique()
                                            )
        df_agrupaciones = df_cargos.query('AP == @agrupaciones')
    with c3: 
        distritos = st.selectbox("Seleccionar distrito:",
                                            df_agrupaciones['Distrito'].unique()
                                            )
        df_distritos = df_agrupaciones.query("Distrito == @distrito")
    with c7: 
        lista = st.selectbox("Seleccionar lista:",
                                            df_distritos['Nombre_lista'].unique()
                                            )
        df_lista = df_distritos.query("Nombre_lista == @lista")

        colores_genero = {
        'M': '#0f203a',
        'F': '#f39a58'
    }
        colores_genero2 = {
        'F': '#0f203a',
        'M': '#0f203a'
    }

    #age_range_gender_counts = df_agrupaciones.groupby(['Age_Range', 'Genero']).size().unstack().reset_index()
    df_lista['Totales'] = 1
    age_range_gender_counts = df_lista.groupby(['Age_Range', 'Genero'])['Totales'].sum().reset_index()
    age_range_gender_counts2 = df_lista.groupby(['Age_Range'])['Totales'].sum().reset_index()
    gender_counts = df_lista.groupby(['Genero'])['Totales'].sum().reset_index()
    barras, pie = st.columns(2)

    tabs_gen = [
                "Por edad y género",
                "Por edad",
                "Por género"]
    tabs_gen2 = [
                "Por edad y género",
                "Por edad","Por género"]


    fig = px.bar(age_range_gender_counts, x='Age_Range', y='Totales', color=age_range_gender_counts['Genero'], color_discrete_map=colores_genero, text=age_range_gender_counts['Totales'])
    fig.update_traces(textposition='outside', textfont_color='black')
    fig.update_xaxes(type='category', ticks="outside", ticklen=5, tickcolor='rgb(195,186,178)', linecolor='rgb(203,193,185)', title='')
    fig.update_yaxes(anchor="free", shift= -10, gridcolor="rgb(228,217,208)", title='')
    fig.update_layout(barmode='group', template='simple_white',            
            title=f"<b>DISTRIBUCIÓN {cargos} DE {agrupaciones} EN {distritos}</b><br><sup>Lista: {lista} - Elecciones PASO 2023</sup>")
        
    fig_edad = px.bar(age_range_gender_counts2, x='Age_Range', y='Totales', text=age_range_gender_counts2['Totales'])
    fig_edad.update_traces(textposition='outside', textfont_color='black', marker=dict(color='#254f8f'))
    fig_edad.update_xaxes(type='category', ticks="outside", ticklen=5, tickcolor='rgb(195,186,178)', linecolor='rgb(203,193,185)', title='')
    fig_edad.update_yaxes(anchor="free", shift= -10, gridcolor="rgb(228,217,208)", title='')
    fig_edad.update_layout(barmode='group', template='simple_white',            
            title=f"<b>{cargos} DE {agrupaciones} EN {distritos}</b><br><sup>Lista: {lista} - Elecciones PASO 2023</sup>")
        
    tabs1, tabs2, tabs3 = st.tabs(tabs_gen)

        #boton_productos = st.radio(
            #"Elegir tipo de gráfico",
            #('Por edad y genero', 'Por edad'), horizontal=True,label_visibility='collapsed')

    with tabs1:
            st.plotly_chart(fig, use_container_width=True)
    with tabs2:
            st.plotly_chart(fig_edad, use_container_width=True)
    with tabs3:
        pie_trace = go.Pie(
            labels=gender_counts['Genero'],
            values=gender_counts['Totales'],
            textinfo='percent+label',
            hoverinfo='label+value',
            textposition='inside',
            marker=dict(colors=['#f39a58', '#0f203a'])
        )

        
        layout2 = go.Layout(
            title=f'GÉNERO {cargos} DE {agrupaciones} EN {distritos}<br><sup>Lista: {lista} - Elecciones PASO 2023</sup>',
            template='simple_white'
        )

        
        fig3 = go.Figure(data=[pie_trace], layout=layout2)
        st.plotly_chart(fig3, use_container_width=True)

    totales_candidatos = df2023_v2 
    totales_candidatos['Totales'] = 1
    totales_gen_edad = totales_candidatos.groupby(['Age_Range', 'Genero'])['Totales'].sum().reset_index()
    totales_edad = totales_candidatos.groupby(['Age_Range'])['Totales'].sum().reset_index()
    gender_counts2 = totales_candidatos.groupby(['Genero'])['Totales'].sum().reset_index()

    st.subheader("Distribución total", help='Cómo se distribuye la suma de todos los precandidatos para todos los cargos en las PASO 2023')



    fig_totales_gen_edad = px.bar(totales_gen_edad, x='Age_Range', y='Totales', color=totales_gen_edad['Genero'], color_discrete_map=colores_genero, text=totales_gen_edad['Totales'])
    fig_totales_gen_edad.update_traces(textposition='outside', textfont_color='black')
    fig_totales_gen_edad.update_xaxes(type='category', ticks="outside", ticklen=5, tickcolor='rgb(195,186,178)', linecolor='rgb(203,193,185)', title='')
    fig_totales_gen_edad.update_yaxes(anchor="free", shift= -10, gridcolor="rgb(228,217,208)", title='')
    fig_totales_gen_edad.update_layout(barmode='group', template='simple_white',            
        title=f"<b>DISTRIBUCIÓN TOTAL POR EDAD Y GÉNERO DE LOS PRECANDIDATOS</b><br><sup>Elecciones PASO 2023</sup>")

    fig_totales_edad = px.bar(totales_edad, x='Age_Range', y='Totales', text=totales_edad['Totales'])
    fig_totales_edad.update_traces(textposition='outside', textfont_color='black', marker=dict(color='#254f8f'))
    fig_totales_edad.update_xaxes(type='category', ticks="outside", ticklen=5, tickcolor='rgb(195,186,178)', linecolor='rgb(203,193,185)', title='')
    fig_totales_edad.update_yaxes(anchor="free", shift= -10, gridcolor="rgb(228,217,208)", title='')
    fig_totales_edad.update_layout(barmode='group', template='simple_white',            
                title=f"<b>DISTRIBUCIÓN TOTAL POR EDAD DE LOS PRECANDIDATOS</b><br><sup>Elecciones PASO 2023</sup>")
            
    tabs4, tabs5, tabs6 = st.tabs(tabs_gen2)

    with tabs4:
                st.plotly_chart(fig_totales_gen_edad, use_container_width=True)
    with tabs5:
                st.plotly_chart(fig_totales_edad, use_container_width=True)     
    with tabs6: 
        data = [
            go.Pie(
                labels=gender_counts2['Genero'],
                values=gender_counts2['Totales'],
                textposition='inside',
                textinfo='percent+label',
                hoverinfo='label+value',
                marker=dict(colors=['#f39a58', '#0f203a'])  
            )
        ]

        
        layout = go.Layout(
            title=f'DISTRIBUCIÓN POR GÉNERO DE LOS PRECANDIDATOS<br><sup>Elecciones PASO 2023</sup>',
            template='simple_white'
        )

        
        fig4 = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig4, use_container_width=True)