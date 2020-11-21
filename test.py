import chains
from pprint import pprint
import json as json
import itertools

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

with open("all.json") as fp:
    table = chains.ProbabilityTable(json.load(fp))

# All print statements have been commented out, they only served as testing utility during development
def cloze_test(rocstories):
    test = chains.load_data(rocstories)
    answers = []
    good_guesses = 0

    for t in test:
        right_answer = story_answer(t)
        one, two = parse_test_instance(t)
        one_pmi = 0
        two_pmi = 0
        one_deps = chains.extract_dependency_pairs(one)
        two_deps = chains.extract_dependency_pairs(two)

        # pprint(one[2:])
        # print("------------")
        for key in one_deps[1]:
            # pprint(one_deps[1][key])
            # print("Every combination for entity ", key, " is:" )
            for element in itertools.combinations(one_deps[1][key], 2):
                # pprint(element)
                one_pmi += table.pmi(element[0][0], element[0][1], element[1][0], element[1][1])
            
        # print("PMI:", one_pmi)
        # print("------------")

        # pprint(two[2:])
        # print("------------")
        for key in two_deps[1]:
            # pprint(two_deps[1][key])
            # print("Every combination for entity ", key, " is:" )
            for element in itertools.combinations(two_deps[1][key], 2):
                # pprint(element)
                two_pmi += table.pmi(element[0][0], element[0][1], element[1][0], element[1][1])
            
        # print("PMI:", two_pmi)
        # print("------------")

        if (one_pmi > two_pmi):
            answers.append((one[0], 1, right_answer[1]))
            if (right_answer[1] == 1):
                good_guesses += 1
        else:
            answers.append((one[0], 2, right_answer[1]))
            if (right_answer[1] == 2):
                good_guesses += 1
    return good_guesses, answers
print(cloze_test("val.csv"))