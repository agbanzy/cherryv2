# File: /cherryAI/user_suggestions.py

from collections import Counter

def get_top_commands(command_history, num_suggestions):
    counter = Counter(command_history)
    return [command for command, _ in counter.most_common(num_suggestions)]
