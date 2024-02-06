
import json
import re
from typing import Any
from rake_nltk import Rake
from pathlib import Path

from searching.preprocessing.ActivityObject import Activity

class LearningEvents:
    """Class to extract and save the lables from the json-file"""

    def __init__(self,
                 data: Path,
                 indicator_list: list[str] = [], 
                 metric_list: list[str] = [], 
                 ranked_metrics_list: list[str] = [], 
                 ranked_metrics_dict: dict[str, int] = {}, 
                 events_list: list[Any] = [], 
                 activities: dict[Any, Any] = {}, 
                 events: Any = {}
            ):
       self.data = open(data)  
       self.indicator_list: list[Any] = indicator_list
       self.metric_list: list[str] = metric_list
       self.ranked_metrics_list: list[Any] = ranked_metrics_list
       self.ranked_metrics_dict: dict[Any, Any] = ranked_metrics_dict
       self.events_list = json.load(self.data)
       self.activities: dict[Any, Any] = activities
       self.events: dict[Any, Any] = events
    
    def get_indicators(self):
        """Function that gets the indicators from the json-file"""
        indicator_list: list[str] = []
        for i in self.events_list: 
            LearningActivities = i["LearningActivities"]
            for j in LearningActivities: 
                indicator = j["indicator"]
                for l in indicator: 
                    # remvoe [] brackets with content from indicator name
                    indicatorName = re.sub(r"\[.*?\]", "", l["indicatorName"])
                    #remove () brackets with content from indicator name
                    indicatorName = re.sub(r"\(.*?\)", "", indicatorName) 
                    #procedure if indicator name contains the word "and"
                    if indicatorName.count("and") >0 :
                        #split indicator at each "and" and use each fragment as own indicator
                        lone_indicators = re.split(" and ", indicatorName)
                        for m in lone_indicators:
                            #make indicator lower case and remove whitespace at the end
                            indicator_list.append(m.lower().rstrip())
                    #procedure if no end is in indicator
                    else:
                        #make indicator lower case and remove whitespace at the end
                        indicator_list.append(indicatorName.lower().rstrip())
        # manually add "srl" and "snl" into list of extracted indicators
        indicator_list.append("srl") 
        indicator_list.append("snl")
        #sort indicator list alphabetically
        indicator_list.sort()
        #remove duplicates from list
        indicator_list = list(set(indicator_list))
        self.indicator_list = indicator_list

    def get_metrics(self):
        """Function that gets the Metrics from the json-file"""

        metric_list: list[str] = []
        for i in self.events_list:
            LearningActivities = i["LearningActivities"]
            for j in LearningActivities: 
                indicator = j["indicator"]
                for l in indicator:
                    metric: str = l["metrics"]
                    # remove [] brackets with content
                    metric = re.sub(r"\[.*?\]", "", metric)
                    # remove () brackets with content
                    metric = re.sub(r"\(.*?\)", "", metric)
                    # split metrics along the "," into a list of single metrics
                    metrics = re.split(",", metric)
                    for n in metrics:
                        # count words inside one metric
                        metric_length = len(re.findall(r'\w+', n))
                        # make metric lower case
                        n = n.lower()
                        # remove whitespaces at the beginning and end of the metrics
                        n = n.strip()
                        # split metric again if it contains "/" and has less then 4 words
                        if n.count("/") > 0 and metric_length < 4:
                            or_list: list[str] = re.split("/", n)
                            for words in or_list:
                                words = words.strip()
                                metric_list.append(words)
                        # split metric again if it contains "&" and has less then 4 words
                        elif n.count("&") > 0 and metric_length <4:
                            and_list = re.split("&", n)
                            for words in and_list:
                                words = words.strip()
                                metric_list.append(words)
                        else:
                            metric_list.append(n)
        metric_list = list(set(metric_list)) 
        metric_list.sort()
        self.metric_list = metric_list
        
    def rank_metrics_list(self):
        """Function to shorten and only add the most important part of each metric to the 
        final search list. All shorter metrics and the parts of the ones rated by rake as
        important are saved inside a list. For the most recent version this function is
        in use."""
        ranked_metrics_list: list[str] = []
        # rake for metrics that contain more then 3 words
        r = Rake()
        # rake for metrics parts that still contain more then three words after first rake
        r2 = Rake()
        for element in self.metric_list:
            # remove "-" since it irritates rake
            element2: str = element.replace("-", " ")
            # counts words in current metric
            metric_length = len(re.findall(r'\w+', element))
            if metric_length < 4:
                # append metrics with 3 or less words to result list without further work
                ranked_metrics_list.append(element)
            # apply rake on metrics with more then 3 words
            else:
                r.extract_keywords_from_text(element2)
                scored_phrases = r.get_ranked_phrases_with_scores()
                for elements in scored_phrases:
                    # count words in resulting metric fragments from rake
                    metricelement_length = metricelement_length = len(re.findall(r'\w+', elements[1]))
                    if metricelement_length > 1 and metricelement_length < 4:
                        # append all rake fragments with more then one word and less then 4 to the result
                        ranked_metrics_list.append(element)
                    # repeat the same step for rake fragment with more than three words
                    elif metricelement_length > 3:
                        r2.extract_keywords_from_text(elements[1])
                        scored_subphrases = r2.get_ranked_phrases_with_scores()
                        for subelements in scored_subphrases:
                            submetricelement_length = len(re.findall(r'\w+', subelements[1]))
                            if submetricelement_length > 1 and submetricelement_length < 4:
                                ranked_metrics_list.append(element)
        # add some additional metrics that contain "-" and are not in the json (please add additional words in lower case to this list)
        additional_Metrics = [ "full-time enrollment", "part-time enrollment", "pre-score", "in-video questions", \
            "college-level education", "left-hand gesture", "right-hand gesture", "pre-survey", "pre-class activities", \
            "problem-solving activities", "pre-test", "post-test", "on-campus connection", "off-campus connection", \
            "text-based data", "animation-based data" ]
        ranked_metrics_list = ranked_metrics_list + additional_Metrics
        ranked_metrics_list.sort()
        ranked_metrics_list = list(set(ranked_metrics_list))
        self.ranked_metrics_list = ranked_metrics_list

    def rank_metrics_dict(self):
        """Function to shorten and only add the most important part of each metric to the 
        final search list. Each metric is safed as a dictionary with the metric name as
        key and the important parts as value inside a list. Function was used for older
        versions but was replaced for the current version by rank_metrics_list()"""
        ranked_metrics_dict = {}
        # rake for metrics that contain more then 3 words
        r = Rake()
        # rake for metrics parts that still contain more then three words after first rake
        r2 = Rake()
        for element in self.metric_list:
            # remove "-" since it irritates rake
            element2 = element.replace("-", " ")
            # counts words in current metric
            metric_length = len(re.findall(r'\w+', element))
            current_metric: list[str] = []
            current_metric.append(element2)
            # append metrics with 3 or less words to result dictionary without further work
            if metric_length < 4:
                ranked_metrics_dict[element] = current_metric
            # apply rake on metrics with more then 3 words
            else:
                r.extract_keywords_from_text(element2)
                scored_phrases = r.get_ranked_phrases_with_scores()
                for elements in scored_phrases:
                    # count words in resulting metric fragments from rake
                    metricelement_length = len(re.findall(r'\w+', elements[1]))
                    # append all rake fragments with more then one word and less then 4 to the results
                    if metricelement_length > 1 and metricelement_length < 4:
                        current_metric.append(elements[1])
                    # repeat the same step for rake fragment with more than three words
                    elif metricelement_length > 3:
                        r2.extract_keywords_from_text(elements[1])
                        scored_subphrases = r2.get_ranked_phrases_with_scores()
                        for subelements in scored_subphrases:
                            submetricelement_length = len(re.findall(r'\w+', subelements[1]))
                            if submetricelement_length > 1 and submetricelement_length < 4:
                                current_metric.append(subelements[1])
                ranked_metrics_dict[element] = current_metric
        # add some additional metrics that contain "-" and are not in the json (please add additional words in lower case to this list)
        additional_Metrics = [ "full-time enrollment", "part-time enrollment", "pre-score", "in-video questions", \
            "college-level education", "left-hand gesture", "right-hand gesture", "pre-survey", "pre-class activities", \
            "problem-solving activities", "pre-test", "post-test", "on-campus connection", "off-campus connection", \
            "text-based data", "animation-based data" ]
        for word in additional_Metrics:
            current_metric = []
            current_metric.append(word)
            ranked_metrics_dict[word] = current_metric
        self.ranked_metrics_dict = ranked_metrics_dict
        
        
    def get_activities(self, activityData:Activity) -> None:
        """Gets the activities and their meta-data from the file Activity Object"""
        self.activities = activityData.activityDictionary
    
        #Old Version that gets activities and the metrics belonging to them from the json:
        #activities = {}
        #for i in self.events_list:
        #    LearningActivities = i["LearningActivities"]
        #    for j in LearningActivities:
        #        curr_activity = j["Name"]
        #        activity_metrics = []
        #        indicator = j["indicator"]
        #        for l in indicator:
        #            curr_metrics = l["metrics"]
        #            curr_metrics = re.sub(r"\[.*?\]", "", curr_metrics)
        #            metrics = re.split(" , ", curr_metrics)
        #            for n in metrics:
        #                activity_metrics.append(n.lower().rstrip())
        #        activity_metrics.sort()
        #        activities[curr_activity] = activity_metrics
        #self.activities = activities

    def get_LearningEvents(self):
        """Functions that gets the events from the json and saves them with the activities
        belonging to them inside a dictionary"""

        events = {}
        for i in self.events_list:
            curr_event = i["LearningEvents"]
            LearningActivities = i["LearningActivities"]
            activity_list: list[str] = []
            for j in LearningActivities:
                activity_list.append(j["Name"])
            events[curr_event] = activity_list
        self.events = events
        
        

