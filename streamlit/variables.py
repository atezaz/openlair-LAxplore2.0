
from pathlib import Path
#import os
from searching.preprocessing import LearningEvents
from searching.preprocessing import Activity

# path to the used json file. Is created dynimacally. If there are any problems please enter it manually into the code for the variable json_path
__parent_folder = Path(__file__).parent
__json_path: Path = Path(__parent_folder, 'LearningEventsJson', 'data.json')
__EventData = LearningEvents(__json_path)
__activityData = Activity()
__EventData.get_indicators()
__EventData.get_metrics()
__EventData.rank_metrics_list()
__EventData.rank_metrics_dict()
__EventData.get_activities(__activityData)
__EventData.get_LearningEvents()

indicators = __EventData.indicator_list
metrics_list = __EventData.ranked_metrics_list
metrics_dict = __EventData.ranked_metrics_dict
activities = __EventData.activities
events = __EventData.events