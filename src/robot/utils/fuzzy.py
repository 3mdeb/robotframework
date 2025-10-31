
import fuzzysearch
from robot.api import logger

def fuzzy_find(buffer, expected, max_substitutions:int=None, max_insertions:int=None, max_deletions:int=None, ignore_case=False):
    found = fuzzy_find_all(buffer, expected, max_substitutions, max_insertions, max_deletions, ignore_case)

    if len(found) > 0:
        return found[0]
    return None

def fuzzy_find_all(buffer, expected, max_substitutions:int=None, max_insertions:int=None, max_deletions:int=None, ignore_case:bool=False):
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

    if max_substitutions is not None:
        try:
            max_substitutions=int(max_substitutions)
        except:
            logger.warn(f"max_substitutions parameter invalid: {max_substitutions}:{type(max_substitutions)}")
            max_substitutions=None

    try:
        if ignore_case:
            matches = fuzzysearch.find_near_matches(subsequence=expected.lower(), sequence=buffer.lower(), max_l_dist=None, max_insertions=max_insertions, max_deletions=max_deletions, max_substitutions=max_substitutions)
            # change matched to contain original, possibly uppercase, input
            for match in matches:
                match.matched = buffer[match.start:match.end]
        else:
            matches = fuzzysearch.find_near_matches(subsequence=expected, sequence=buffer, max_l_dist=None, max_insertions=max_insertions, max_deletions=max_deletions, max_substitutions=max_substitutions)
        return matches

    except Exception as e:
        logger.error(e)
        logger.error("max_substitutions: ", max_substitutions, ": ", type(max_substitutions))
        logger.error("max_insertions: ", max_insertions, ": ", type(max_insertions))
        logger.error("max_deletions: ", max_deletions, ": ", type(max_deletions))
        logger.error("ignore_case: ", ignore_case, ": ", type(ignore_case))
        logger.error("\n\n\nexpected:")
        logger.error(expected)
        logger.error("\n\n\nbuffer:")
        logger.error(buffer)

