
import re
import operator
# from searching.preprocessing import PdfFile
# from searching.preprocessing import LearningEvents

class FoundIndicators:
    """Represents the indicators found in the text and their occurence."""

    def __init__(self, article: str, indicatorNames: list[str], foundNames: dict[str, int] = {}):
        self.article = article
        self.indicatorNames = indicatorNames
        self.foundNames = foundNames

    def search_indicators(self):
        foundNames: dict[str, int] = {}
        for i in self.indicatorNames:
            space_count = i.count(" ")
            or_count = i.count(" or ")
            # if indicator has an "or" inside it it gets split and the occurence is counted for both halfs and added
            if or_count > 0:
                or_tokens = re.split(" or ", i)
                occurence = self.article.count(or_tokens[0] + or_tokens[1])
            # indicators made up of 3 words are put into a list together with all two word combinations that can be made out of them
            elif space_count == 2 :
                indicator_variations: list[str] = []
                indicator_variations.append(i)
                split_indicator = re.split(" ", i)
                indicator_variations.append(split_indicator[0] + " " + split_indicator[1])
                indicator_variations.append(split_indicator[0] + " " + split_indicator[2])
                indicator_variations.append(split_indicator[1] + " " + split_indicator[2])
                occurence = 0
                # occurence sum for all three words and two word combinations is calculated
                for j in indicator_variations:
                    occurence += self.article.count(j)
                # the count of the entire indicator name needs to be subtracted twice since indicator_variations[1] and indicator_variations[3] count it as well
                occurence = occurence - 2 * self.article.count(indicator_variations[0])
            else:
                occurence = self.article.count(i)
            if occurence > 0:
                foundNames[i] = occurence
        # dictionary with found indicators and their occurence is sorted by occurences
        foundNames_sorted: dict[str, int] = dict(sorted(foundNames.items(), key=operator.itemgetter(1), reverse=True))
        self.foundNames = foundNames_sorted
        
    
    

