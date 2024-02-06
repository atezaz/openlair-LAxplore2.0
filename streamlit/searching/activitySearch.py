
import re
# from searching import metricSearch
# from searching.preprocessing import PdfFile
# from searching.preprocessing import LearningEvents



class FoundActivities:
    """Represents Activities, the meta data belonging to them and the occurence of each activity 
    found in the text"""
    
    def __init__(self, 
                 activities: dict[str, list[str]], 
                 article: str, 
                 foundActivities: list[str] = [], 
                 foundActivitiesWithMetaData: dict[str, list[str]] = {}, 
                 occurence_list: list[int] = []):
        self.activities = activities
        self.article = article
        self.foundActivities = foundActivities
        self.foundActivitiesWithMetaData = foundActivitiesWithMetaData
        self.occurence_list = occurence_list

    def search_activities(self):
        """Looks in the selected PDF for the meta data and the sum of the occurences of the meta data per article"""

        foundActivities: list[str] = []
        foundActivitiesWithMetaData_list: dict[str, list[str]] = {}
        foundActivitiesWithMetaData_string = {}
        occurence_list: list[int] = []
        # looping through the meta data of each activity
        for i,j in self.activities.items():
            found_activity_metaData: list[str] = []
            current_activity = i
            activity_meta_data = j
            occurence = 0
            for l in activity_meta_data:
                # count how often the current meta-data element appears in the article
                current_occurence = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(l), self.article))
                occurence += current_occurence
                # appends meta data into a list if it's occurence is > 0
                if current_occurence > 0:
                    found_activity_metaData.append(l)
            # if occurence is greater 2 the activity will be safed together with its appearing meta data in a dictionary
            # the occurence sum is also saved in but in a separate list for each found activity
            if occurence > 1:
                occurence_list.append(occurence)
                foundActivities.append(current_activity)
                foundActivitiesWithMetaData_list[current_activity] = found_activity_metaData
        # turn dictionary values containing found meta-data from list into a string where they are speparated by ", " in order to prevent problems in the visualisation with st.table
        for activity, meta_data in foundActivitiesWithMetaData_list.items():
            meta_data = ", ".join(meta_data)
            foundActivitiesWithMetaData_string[activity] = meta_data
        self.foundActivities = foundActivities
        self.foundActivitiesWithMetaData = foundActivitiesWithMetaData_list
        self.occurence_list = occurence_list
            