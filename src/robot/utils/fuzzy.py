
import fuzzysearch

def fuzzy_find(buffer, expected, percent_match=None, max_errors=None, max_insertions:int=None, max_deletions:int=None, ignore_case=False):
    found = fuzzy_find_all(buffer, expected, percent_match, max_errors, max_insertions, max_deletions, ignore_case)

    if len(found) > 0:
        return found[0]
    return None

def fuzzy_find_all(buffer, expected, percent_match:float=None, max_errors:int=None, max_insertions:int=None, max_deletions:int=None, ignore_case:bool=False):
    
    if max_insertions:
        max_insertions=int(max_insertions)
    if max_deletions:
        max_deletions=int(max_deletions)
    if max_errors is not None:
        max_errors = int(max_errors)
        max_l_dist = max_errors
    elif percent_match is not None:
        percent_match = float(percent_match)
        percent_match = min(100, max(0, percent_match)) # limit to 0-100
        percent_errors = 100 - percent_match
        max_l_dist = round(len(expected) * percent_errors / 100.0)
    else:
        max_l_dist = None
    

    if ignore_case:
        matches = fuzzysearch.find_near_matches(expected.lower(), buffer.lower(), max_l_dist=max_l_dist, max_insertions=max_insertions, max_deletions=max_deletions)
        # change matched to contain original, possibly uppercase, input
        for match in matches:
            match.matched = buffer[match.start:match.end]
    else:
        matches = fuzzysearch.find_near_matches(expected, buffer, max_l_dist=max_l_dist, max_insertions=max_insertions, max_deletions=max_deletions)
    return matches
