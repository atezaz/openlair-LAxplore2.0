import pandas as pd
import re
from typing import overload

class FoundMetricSentences:
    """Class that takes the metrics selected on the streamlit page and looks for the sentences containing them in the text"""

    def __init__(self, article, metric_table, metric_sentences = {}):
        self.article = article
        self.metric_table = metric_table
        self.metric_sentences = metric_sentences

    @overload
    def get_msentences(self):
        ...
    
    @overload
    def get_msentences(self, metric_indices: list[int]):
        ...
        
    def get_msentences(self, metric_indices = None):
        """This function gets the sentences containing the metrics"""
        if (metric_indices):
            selected_metrics = self.metric_table.loc[metric_indices]
        else:
            selected_metrics = self.metric_table
        metric_sentences = {}
        # extracting the metric names from the table that was created
        selected_metrics = selected_metrics["Metric"].to_list()
        for metric in selected_metrics:
            actual_sentences = []
            # regex to extract all sentences into a list that contain the word that is looked for
            #found_sentences = re.findall(r"([^.!?]*?%s.[^.!?]*[.!?])" %metric, self.article ) -> first version
            #found_sentences = re.findall(r"(([^.!?]|(\d+.\d+))*?%s.*?[^.!?]*[.!?](?=\s))" %metric, self.article) -> version which archieves best results but ends the program without error message due to catastrophic backtracking
            found_sentences = re.findall(r"([^.!?:]*?%s.*?[^.!?:]*[.!?:](?=\s))" %metric, self.article) # current best version that does not cause catastrophic backtracking
            # extra loop that makes sure only sentences are added to the result, where the metric exactly as in the table the function got
            for sentence in found_sentences:
                #if re.search(r"\b"+metric+r"\b", sentence):
                if re.search(r'\b%s' % re.escape(metric), sentence):
                    #make metric upper case to higlight it
                    sentence = sentence.replace(metric, metric.upper())
                    actual_sentences.append(sentence)
            metric_sentences[metric] = actual_sentences
        self.metric_sentences = metric_sentences