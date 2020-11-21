import chains
from pprint import pprint
import json as json

def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding

test = chains.load_data("val.csv")

for t in test:
    one, two = parse_test_instance(t)
    one_deps = chains.extract_dependency_pairs(one)
    two_deps = chains.extract_dependency_pairs(two)
    pprint(one[2:])
    pprint(one_deps)
    pprint(two[2:])
    pprint(two_deps)
    # logic to choose between one and two
    # pprint("answer:"+ str(story_answer(t)))