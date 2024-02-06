import pandas as pd
import re
from typing import overload

class FoundIndicatorSentences:
    """Class that takes the indicators selected on the streamlit page and looks for the sentences containing them in the text"""

    def __init__(self, article, indicator_table, indicator_sentences = {}):
        self.article = article
        self.indicator_table = indicator_table
        self.indicator_sentences = indicator_sentences

    @overload
    def get_isentences(self):
        ...
    
    @overload
    def get_isentences(self, indicator_indices: list[int]):
        ...
        
    def get_isentences(self, indicator_indices = None):
        """This function gets the sentences containing the indicators"""
        if (indicator_indices):
            selected_indicators = self.indicator_table.loc[indicator_indices]["Indicator"].to_list()
        else:
            selected_indicators = self.indicator_table["Indicator"].to_list()
            
        indicator_sentences = {}
        # extracting the indicator names from the table that was created
        for indicator in selected_indicators:
            found_sentences = []
            found_sentenceshighlighted = []
            indicator_length = indicator.count(" ")
            # looking for all variations of the indicator (since it was also searched that way in the text)
            if indicator_length >= 2:
                indicator_variations = []
                indicator_variations.append(indicator)
                split_indicator = re.split(" ", indicator)
                indicator_variations.append(split_indicator[0] + " " + split_indicator[1])
                indicator_variations.append(split_indicator[0] + " " + split_indicator[2])
                indicator_variations.append(split_indicator[1] + " " + split_indicator[2])
                for variation in indicator_variations:
                    # regex to extract all sentences into a list that contain the word that is looked for
                    #found_sentences += re.findall(r"([^.!?]*?%s.[^.!?]*[.!?])" %variation, self.article) -> first version
                    #found_sentences = re.findall(r"(([^.!?]|(\d+.\d+))*?%s.*?[^.!?]*[.!?](?=\s))" %variation, self.article) -> version which archieves best results but ends the program without error message due to catastrophic backtracking
                    #found_sentences += re.findall(r"([^.!?:]*?%s.*?[^.!?:]*[.!?:](?=\s))" %variation, self.article) # current best version that does not cause catastrophic backtracking
                    found_sentences = re.findall(r"([^.!?:]*?%s.*?[^.!?:]*[.!?:](?=\s))" %variation, self.article) # current best version that does not cause catastrophic backtracking
                    for sentence in found_sentences:
                        if variation == indicator_variations[0]:
                            sentence = sentence.replace(variation, variation.upper())
                            found_sentenceshighlighted.append(sentence)
                        else:
                            # makes sure to only highlight indicator variations that are not the entire name if the entire indicator name does not appear in the sentence
                            if indicator_variations[0] not in sentence:
                                sentence = sentence.replace(variation, variation.upper())
                                found_sentenceshighlighted.append(sentence)

            else:
                # regex to extract all sentences into a list that contain the word that is looked for
                #found_sentences = re.findall(r"([^.!?]*?%s.[^.!?]*[.!?])" %indicator, self.article) -> first version
                #found_sentences = re.findall(r"(([^.!?]|(\d+.\d+))*?%s.*?[^.!?]*[.!?](?=\s))" %indicator, self.article) -> version which archieves best results but ends the program without error message due to catastrophic backtracking
                #found_sentences += re.findall(r"([^.!?:]*?%s.*?[^.!?:]*[.!?:](?=\s))" %indicator, self.article) # current best version that does not cause catastrophic backtracking
                found_sentences = re.findall(r"([^.!?:]*?%s.*?[^.!?:]*[.!?:](?=\s))" %indicator, self.article) # current best version that does not cause catastrophic backtracking
                for sentence in found_sentences:
                    sentence = sentence.replace(indicator, indicator.upper())
                    found_sentenceshighlighted.append(sentence)
            indicator_sentences[indicator] = found_sentenceshighlighted
        self.indicator_sentences = indicator_sentences

 # explain when not appears.           
