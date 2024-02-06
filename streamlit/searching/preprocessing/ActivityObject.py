
class Activity:
    """Class that creates statically a dictionary/object for the activities and their meta data.
    This is then used to search activities inside the text. Meta data should be written here in
    lower case since all the content in the PDF is also turned into lower case."""

    def __init__(self, activityDictionary = {}):
        self.activityDictionary = {"Design" : ["design", "designing", "plan","planning","create","creating"],\
            "Group work" : ["group work", "teamwork"], "collaboration" : ["collaboration", "cooperation"], \
            "Reading" : ["reading", "read"], "Review/Study" : ["review"], "Watching (videos)" : ["watching videos", \
            "watching video", "video watching", "videos watching", "watch video", "watch videos", "videos", "video", \
            "watching", "watch", "Video-Watching"], "Presentation" : ["presentation", "present"], "Rating/Ranking" : \
            ["rating", "ranking", "rate", "rank"], "Exercise (Training)" : ["exercise", "exercises", "student training", "train student", "train students", "user training", "train user", "train users"], \
            "Presentation" : ["presentation", "present"], "Examine" : ["examine", "explore"], "Survey" : \
            ["survey", "surveys", "questionaire", "questionaires"], "Search" : ["search", "searching", "seek", \
            "seeking", "looking", "look", "looking for", "look for"], \
            "Procedural actions (keystroke, hits/clicks, clickstream, views, visits, interactions, downloads)" : \
            ["keystroke", "keystrokes", "hits", "clicks", "clickstream", "views", "visits", "interactions", \
            "interaction", "download", "downloads"], "Game or puzzle" : ["game", "gaming", "puzzle"], \
            "Problem solving" : ["problem-solving", "problem solving", "solve problem", "solve problems"], \
            "Exercise (Training)" : ["exercise", "exercises", "student training", "train student", "train students", "user training", "train user", "train users"], "Exam" : ["exam", "exams"], \
            "Test" : ["test", "tests"], "Quiz" : ["quiz", "quizzes"], "Exercise (Training)" : \
            ["exercise", "exercises", "student training", "train student", "train students", "user training", "train user", "train users"], "Task" : ["task", "tasks"], "Writing" : \
            ["writing", "writes", "write"], "Group Work" : ["group work", "teamwork"], "Peer review/Assessment" : \
            ["peer review", "assessment", "evaluation", "evaluate", "judge", "judging"], "Assignment/homework" : \
            ["assignment", "homework"], "Question (Query/Inquiry)" : ["query", "queries", "question", "questions"],\
            "Survey(Questionnaire)" : ["survey", "surveys", "questionnaire", "questionnaires"], "Feedback" : \
            ["feedback", "response"], "Rating/ranking" : ["rating", "ranking", "rate", "rank"], \
            "Self-learning / reporting" : ["self-learning", "self learning", "self-learn", "self learn", \
            "self-reporting", "self-report", "self reporting", "self report"], "Analysis" : ["analysis", \
            "examination", "inspection", "inquiry", "analyses", "scrutinize", "scrutinise", "analyze", "analyzing", \
            "inquire"], "Peer review/Assessment" : ["peer review", "assessment", "evaluation", "evaluate", "judge", \
            "judging"], "Review/ Study" : ["review"], "Forum discussion" : ["forum discussion", "discussion"], \
            "Group work" : ["group work", "teamwork"], "Comments" : ["comments", "comment", "commenting"], \
            "Posts" : ["posts", "post", "posting"], "Discourse" : ["discourse", "dialogue"], "Review / Study" : \
            ["review"], "Question (Query/Inquiry)" : ["query", "queries", "question", "questions"], "Survey (Questionnaire)" :\
            ["survey", "surveys", "questionnaire", "questionnaires"], "Presentation" : ["presentation", \
            "present"], "Vote(poll)" : ["vote", "poll", "votes", "polls", "voting", "polling"]}