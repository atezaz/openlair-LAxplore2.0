import pandas as pd
import json

from searching.activitySearch import FoundActivities
from searching.eventSearch import FoundEvents
from searching.indicatorSentences import FoundIndicatorSentences
from searching.metricSearch import FoundMetrics
from searching.metricSentences import FoundMetricSentences
from streamlit.runtime.uploaded_file_manager import UploadedFile
import variables
from searching.indicatorSearch import FoundIndicators
from searching.preprocessing.DataExtraction import PdfFile

from werkzeug.datastructures.file_storage import FileStorage
from typing import overload, Union,Optional,Callable


class ProcessedPDF():
    
    @overload
    def __init__(self, file: FileStorage) -> None:
        ...
    
    
    @overload
    def __init__(self, file: UploadedFile) -> None:
        ...
    
    def __init__(self, file: Union[UploadedFile, FileStorage]) -> None:
        if hasattr(file, "filename"):
            self.name: Optional[str] = getattr(file, "filename")
        else:
            self.name: Optional[str] = file.name
        self.Pdf_data = PdfFile(file)
        self.Pdf_data.extract()

        Pdf_indicators = FoundIndicators(self.Pdf_data.content, variables.indicators)
        Pdf_indicators.search_indicators()
        indicators = list(Pdf_indicators.foundNames.keys())
        indicator_occurences = list(Pdf_indicators.foundNames.values())
        # table for found indicators with indicator names and occurences as collumns
        self.indicator_result = pd.DataFrame(
            {
                "Indicator": indicators,
                "Occurence": indicator_occurences
                }
            )
        self.IndicatorsInText = FoundIndicatorSentences(self.Pdf_data.content, self.indicator_result)


        Pdf_metrics = FoundMetrics(self.Pdf_data.content, variables.metrics_list, variables.metrics_dict)
        Pdf_metrics.serch_metrics_listMethod()
        metrics = list(Pdf_metrics.foundMetrics.keys())
        metric_occurences = list(Pdf_metrics.foundMetrics.values())
        # table for found metrics with metric names and occurences as collumns
        self.metric_result = pd.DataFrame(
            {
                "Metric": metrics,
                "Occurence": metric_occurences
                }
            )
        self.MetricsInText = FoundMetricSentences(self.Pdf_data.content, self.metric_result)



        Pdf_activities = FoundActivities(variables.activities, self.Pdf_data.content)
        Pdf_activities.search_activities()
        activities = list(Pdf_activities.foundActivitiesWithMetaData.keys())
        meta_data = list(Pdf_activities.foundActivitiesWithMetaData.values())
        #table for found activities with activities, found meta-data and occurences as collumns
        activity_result: pd.DataFrame = pd.DataFrame(
            {
                "Activity": activities,
                "Meta-Data" : meta_data,
                "Occurence" : Pdf_activities.occurence_list
                }
            )
        # sort activities by occurence
        self.activity_result = activity_result.sort_values(by=["Occurence"], ascending=False)


        Pdf_events = FoundEvents(variables.events, Pdf_activities.foundActivities, Pdf_activities.occurence_list)
        Pdf_events.search_Events()
        events: list[str] = list(Pdf_events.foundEventswithActivities.keys())
        event_activities: list[str] = list(Pdf_events.foundEventswithActivities.values())
        #table for found events with events and found activities for each event as collumns
        event_result: pd.DataFrame = pd.DataFrame(
            {
                "Event": events,
                "Activities belonging to the Event": event_activities,
                "Occurence": Pdf_events.event_occurence
                }
            )
        #sort events by occurence
        self.event_result = event_result.sort_values(by=["Occurence"], ascending=False)


    def get_all_sentences(self):
        self.MetricsInText.get_msentences()
        self.IndicatorsInText.get_isentences()


    def toJson(self): 
        return {
            "indicators": \
                dict(zip(self.indicator_result["Indicator"].to_list(), self.indicator_result["Occurence"].to_list())),
            "indicator_sentences": \
                self.IndicatorsInText.indicator_sentences,
            "metrics": \
                dict(zip(self.metric_result["Metric"].to_list(), self.metric_result["Occurence"].to_list())),
            "metric_sentences": \
                self.MetricsInText.metric_sentences,
            # "activities": dict(zip(
            #     self.activity_result["Activity"].to_list(),
            #     map((lambda item: [item[0], item[1]]), zip( 
            #         self.activity_result["Meta-Data"].to_list(),
            #         self.activity_result["Occurence"].to_list()
            #     ))
            # )),
            "activities": dict([
                [row["Activity"], [row["Meta-Data"], row["Occurence"]]] for _, row in self.activity_result.iterrows()
            ]),
            # "events": dict(zip(
            #     self.event_result["Event"].to_list(),
            #     map((lambda item: [item[0], item[1]]), zip( 
            #         self.event_result["Activities belonging to the Event"].to_list(),
            #         self.event_result["Occurence"].to_list()
            #     ))
            # )),
            "events": dict([
                [row["Event"], [row["Activities belonging to the Event"], row["Occurence"]]] for _, row in self.event_result.iterrows()
            ])


        }