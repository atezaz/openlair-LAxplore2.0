# external modules
import streamlit as st
import pandas as pd

# own modules
from searching.processedPdf import ProcessedPDF

# type realted modules
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile

pdf: Optional[ProcessedPDF] = None

# def parse_pdf(file) -> tuple[PdfFile, pd.DataFrame, FoundIndicatorSentences, pd.DataFrame, FoundMetricSentences, pd.DataFrame, pd.DataFrame]:
#     Pdf_data = PdfFile(file)
#     Pdf_data.extract()

#     Pdf_indicators = FoundIndicators(Pdf_data.content, variables.indicators)
#     Pdf_indicators.search_indicators()
#     indicators = list(Pdf_indicators.foundNames.keys())
#     indicator_occurences = list(Pdf_indicators.foundNames.values())
#     # table for found indicators with indicator names and occurences as collumns
#     indicator_result = pd.DataFrame(
#         {
#             "Indicator": indicators,
#             "Occurence": indicator_occurences
#             }
#         )
#     IndicatorsInText = FoundIndicatorSentences(Pdf_data.content, indicator_result)


#     Pdf_metrics = FoundMetrics(Pdf_data.content, variables.metrics_list, variables.metrics_dict)
#     Pdf_metrics.serch_metrics_listMethod()
#     metrics = list(Pdf_metrics.foundMetrics.keys())
#     metric_occurences = list(Pdf_metrics.foundMetrics.values())
#     # table for found metrics with metric names and occurences as collumns
#     metric_result = pd.DataFrame(
#         {
#             "Metric": metrics,
#             "Occurence": metric_occurences
#             }
#         )
#     MetricsInText = FoundMetricSentences(Pdf_data.content, metric_result)



#     Pdf_activities = FoundActivities(variables.activities, Pdf_data.content)
#     Pdf_activities.search_activities()
#     activities = list(Pdf_activities.foundActivitiesWithMetaData.keys())
#     meta_data = list(Pdf_activities.foundActivitiesWithMetaData.values())
#     #table for found activities with activities, found meta-data and occurences as collumns
#     activity_result: pd.DataFrame = pd.DataFrame(
#         {
#             "Activity": activities,
#             "Meta-Data" : meta_data,
#             "Occurence" : Pdf_activities.occurence_list
#             }
#         )
#     # sort activities by occurence
#     activity_result = activity_result.sort_values(by=["Occurence"], ascending=False)


#     Pdf_events = FoundEvents(variables.events, Pdf_activities.foundActivities, Pdf_activities.occurence_list)
#     Pdf_events.search_Events()
#     events: list[str] = list(Pdf_events.foundEventswithActivities.keys())
#     event_activities: list[str] = list(Pdf_events.foundEventswithActivities.values())
#     #table for found events with events and found activities for each event as collumns
#     event_result: pd.DataFrame = pd.DataFrame(
#         {
#             "Event": events,
#             "Activities belonging to the Event": event_activities,
#             "Occurence": Pdf_events.event_occurence
#             }
#         )
#     #sort events by occurence
#     event_result = event_result.sort_values(by=["Occurence"], ascending=False)

#     return Pdf_data, indicator_result, IndicatorsInText ,metric_result, MetricsInText, activity_result, event_result


def renderPage():
    """Creates the page that visualizes the results"""
    global pdf
    st.title("Data in text")
    

    # file uploader for pdf
    uploaded_file: Optional[UploadedFile] = st.file_uploader("Choose a PDF file you want to analyze", type = "pdf") # type: ignore
    
    if st.checkbox("Search this text") and uploaded_file:
    #if st.button("Search") and uploaded_file is not None:
        if not uploaded_file:
            return
        if not pdf or pdf.name != uploaded_file.name:
            pdf = ProcessedPDF(uploaded_file)

        st.write("Table with the results for the found Indicators")
        st.dataframe(pdf.indicator_result)
        #st.table(indicator_result)
        # Streamlit form to get the sentences containing the indicators without having to reload the page
        indicator_form = st.form(key='ind_form')
        indicator_indices = indicator_form.multiselect("Select rows of the indicators which you want to see inside the pdf", pdf.indicator_result.index)
        confirmation_ind = indicator_form.form_submit_button("Confirm choice")
        if confirmation_ind:
            pdf.IndicatorsInText.get_isentences(indicator_indices)
            indicator_form.write(pdf.IndicatorsInText.indicator_sentences)

        st.write("Table with the results for found Metrics")
        st.dataframe(pdf.metric_result)
        #st.table(metric_result)
        # Streamlit form to get the sentences containing the metrics without having to reload the page
        metric_form = st.form(key='met_form')
        metric_indices = metric_form.multiselect("Select rows of the metrics which you want to see inside the pdf", pdf.metric_result.index)
        confirmation_met = metric_form.form_submit_button("Confirm choice")
        # if metric_indices.
        if confirmation_met:
            pdf.MetricsInText.get_msentences(metric_indices)
            metric_form.write(pdf.MetricsInText.metric_sentences)

        st.write("Table with the results for found Activities")
        # writes table for Activities and removes index that is in wrong order
        st.table(pdf.activity_result.assign(no_index='').set_index('no_index'))

        st.write("Table with the results for found Events")
        # writes table for events and removes index that is in wrong order
        st.table(pdf.event_result.assign(no_index='').set_index('no_index'))
    








