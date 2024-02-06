
# from searching import metricSearch
# from searching.activitySearch import FoundActivities
# from searching.preprocessing import PdfFile
# from searching.preprocessing import LearningEvents

class FoundEvents:
    """Represents the events and the activities belonging to each event found in the text"""
    
    def __init__(
                self, 
                events: dict[str, list[str]], 
                found_activities: list[str], 
                activity_occurence: list[int], 
                foundEvents: list[str] = [], 
                foundEventswithActivities: dict[str, str] = {}, 
                event_occurence: list[int] = []):
        self.events = events
        self.found_activities = found_activities
        self.activity_occurence = activity_occurence
        self.foundEvents = foundEvents
        self.foundEventswithActivities = foundEventswithActivities
        self.event_occurence = event_occurence

    def search_Events(self):
        """Works with a dictionary containing all events and the activities belonging to them.
        Compares it with the activities found in the text and saves all events together with the
        activities that were found for them into a new dictionary"""
        foundEvents: list[str] = []
        foundEventswithActivities_list: dict[str, list[str]] = {}
        foundEventswithActivities_string = {}
        event_occurence: list[int] = []
        for i,j in self.events.items():
            found_event_activities: list[str] = []
            current_event = i
            activities = j
            occurence = 0
            # checks if each activity for the current event is inside the found_activities dictionary
            for l in activities:
                if l in self.found_activities:
                    found_event_activities.append(l)
                    # gets index of found activity to also get it's occurence in the list activity_occurence
                    occurence_index = self.found_activities.index(l)
                    # gets event occurence by summing up the occurence of all activities that were found and belong to the current event
                    occurence += self.activity_occurence[occurence_index]
            if len(found_event_activities) > 0:
                foundEvents.append(current_event)
                foundEventswithActivities_list[current_event] = found_event_activities
                event_occurence.append(occurence)
        # turn dictionary values containing found activities belonging to events from list into a string where they are speparated by ", " in order to prevent problems in the visualisation with st.table
        for events, event_activities in foundEventswithActivities_list.items():
            event_activities = ", ".join(event_activities)
            foundEventswithActivities_string[events] = event_activities
        self.foundEvents = foundEvents
        self.foundEventswithActivities = foundEventswithActivities_list
        self.event_occurence = event_occurence

         