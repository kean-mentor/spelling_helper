import random


question_mode = ['is_correct', 'fill_empty']
letters = ['j', 'ly']


def prepare_question(words, question_list):
    # Select a new question
    question = random.choice(words)
    while question in question_list:
        question = random.choice(words)

    # Select question mode
    qm = random.choice(question_mode)
    if qm == 'is_correct':
        # Randomly swap 'j' with 'ly' or vice versa
        trivia  = question.replace('j', random.choice(letters)).replace('ly', random.choice(letters))
    else:
        # Replace 'j' and 'ly' with underscores
        trivia = question.replace('j', '_').replace('ly', '_')

    return {'q': trivia, 'qm': qm, 'a': question}

def check_answer(question, answer):
    if question['qm'] == 'is_correct':
        if (answer == 'yes' and question['q'] == question['a']) or (answer == 'no' and question['q'] != question['a']):
            return True
        return False
    else:
        user_answer = question['q'].replace('_', answer)
        if user_answer == question['a']:
            return True
        return False
