def check(process_output, judge_output, **kwargs):
    from itertools import izip
    from string import split
    token = kwargs.get('token', '\n')
    process_tokens = filter(None, process_output.split(token))
    judge_tokens = filter(None, judge_output.split(token))
    if len(process_tokens) != len(judge_tokens):
        return False
    process_tokens = map(split, process_tokens)
    judge_tokens = map(split, judge_tokens)
    process_tokens.sort()
    judge_tokens.sort()
    for process_token, judge_token in izip(process_tokens, judge_tokens):
        if process_token != judge_token:
            return False
    return True
