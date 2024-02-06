
import re
import operator
# from searching.preprocessing import PdfFile
#from preprocessing import PdfFile
# from searching.preprocessing import LearningEvents
#from preprocessing import LearningEvents

class FoundMetrics:
    """Represents the metrics found in the text and their occurence"""

    def __init__(self, article: str, ranked_metrics_list: list[str] , ranked_metrics_dict: dict[str, list[str]], foundMetrics: dict[str, int] = {}):
        self.article = article
        self.ranked_metrics_list = ranked_metrics_list
        self.ranked_metrics_dict = ranked_metrics_dict
        self.foundMetrics = foundMetrics
        
     
    def serch_metrics_listMethod(self):
        """Searches the metrics and/or the parts of them rake rated as important and counts their
        occurence. Current version that loops through the metrics saved inside a list."""
        foundMetrics: dict[str, int] = {}
        # loops through list and counts occurence of every metric
        for i in self.ranked_metrics_list:
            #occurence = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(i), self.article))
            # makes sure occurence is only counted if current metric is not a substring in the middle of a actual word
            occurence = sum(1 for _ in re.finditer(r'\b%s' % re.escape(i), self.article))
            if occurence > 0:
                foundMetrics[i] = occurence
        # sorts results by occurence
        sorted_metrics = dict(sorted(foundMetrics.items(), key=operator.itemgetter(1), reverse=True))
        self.foundMetrics = sorted_metrics

        
    def search_metrics_dictMethod(self):
        """Searches the metrics and/or the parts of them rake rated as important and counts their
        occurence. Old version that loops through the metrics saved inside a dictionary. Not called
        in the current version of the code."""

        foundMetrics: dict[str, int] = {}
        for i, j in self.ranked_metrics_dict.items():
            occurence = 0
            metric_name = i
            searchwords = j
            # counts the occurence of each searchword per metric (either metric itself or rake fragment)
            for l in searchwords:
                # makes sure occurence is only counted when a substring inside the text is the exact same as the searchword
                occurence += sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(l), self.article))
            if occurence > 0:
                foundMetrics[metric_name] = occurence
        # sorts result by occurence
        sorted_metrics = dict(sorted(foundMetrics.items(), key=operator.itemgetter(1), reverse=True))
        self.foundMetrics = sorted_metrics
