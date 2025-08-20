
import fuzzysearch
from robot.api import logger

def fuzzy_find(buffer, expected, percent_match=None, max_errors=None, max_insertions:int=None, max_deletions:int=None, ignore_case=False):
    found = fuzzy_find_all(buffer, expected, percent_match, max_errors, max_insertions, max_deletions, ignore_case)

    if len(found) > 0:
        return found[0]
    return None

def fuzzy_find_all(buffer, expected, percent_match:float=None, max_errors:int=None, max_insertions:int=None, max_deletions:int=None, ignore_case:bool=False):
    max_l_dist = 0

    if max_insertions is not None:
        try:
            max_insertions=int(max_insertions)
        except:
            logger.warn(f"max_insertions parameter invalid: {max_insertions}:{type(max_insertions)}")
            max_insertions=None

    if max_deletions is not None:
        try:
            max_deletions=int(max_deletions)
        except:
            logger.warn(f"max_deletions parameter invalid: {max_deletions}:{type(max_deletions)}")
            max_deletions=None

    if max_errors is not None:
        try:
            max_errors = int(max_errors)
            max_l_dist = max_errors
        except:
            logger.warn(f"max_errors parameter invalid: {max_errors}:{type(max_errors)}")
            max_errors=None
    elif percent_match is not None:
        try:
            percent_match = float(percent_match)
            percent_match = min(100, max(0, percent_match)) # limit to 0-100
            percent_errors = 100 - percent_match
            max_l_dist = int(round(len(expected) * percent_errors / 100.0))
        except:
            logger.warn(f"percent_match parameter invalid: {percent_match}:{type(percent_match)}")
            percent_match=None
    try:
        if ignore_case:
            matches = fuzzysearch.find_near_matches(subsequence=expected.lower(), sequence=buffer.lower(), max_l_dist=max_l_dist, max_insertions=max_insertions, max_deletions=max_deletions, max_substitutions=0)
            # change matched to contain original, possibly uppercase, input
            for match in matches:
                match.matched = buffer[match.start:match.end]
        else:
            matches = fuzzysearch.find_near_matches(subsequence=expected, sequence=buffer, max_l_dist=max_l_dist, max_insertions=max_insertions, max_deletions=max_deletions, max_substitutions=0)
        return matches
    except Exception as e:
        logger.error(e)
        logger.error("percent_match: ", percent_match, ": ", type(percent_match))
        logger.error("max_errors: ", max_errors, ": ", type(max_errors))
        logger.error("max_insertions: ", max_insertions, ": ", type(max_insertions))
        logger.error("max_deletions: ", max_deletions, ": ", type(max_deletions))
        logger.error("ignore_case: ", ignore_case, ": ", type(ignore_case))
        logger.error("\n\n\nexpected:")
        logger.error(expected)
        logger.error("\n\n\nbuffer:")
        logger.error(buffer)
    
