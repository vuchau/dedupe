#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from zope.index.text.parsetree import ParseError

logger = logging.getLogger(__name__)

class TfidfPredicate(object):
    def __init__(self, threshold, field):
        self.__name__ = 'TF-IDF:' + str(threshold) + field
        self.field = field
        self.canopy = None
        self.threshold = threshold

    def __repr__(self) :
        return self.__name__

    def __call__(self, record) :
        record_id = record[0]
        center = self.canopy[record_id]
        if center :
            return (unicode(center),)
        else :
            return ()






#@profile
def makeCanopy(index, token_vector, threshold) :
    canopies = {}
    seen = set([])
    corpus_ids = set(token_vector.keys())

    while corpus_ids:
        center_id = corpus_ids.pop()
        center_vector = token_vector[center_id]

        seen.add(center_id)
        
        if not center_vector :
            continue

        try :
            search_string = ' OR '.join(center_vector)
            candidates = index.apply(search_string).byValue(threshold)
        except ParseError :
            continue

        candidates = set(k for  _, k in candidates) - seen

        seen.update(candidates)
        corpus_ids.difference_update(candidates)

        for candidate_id in candidates :
            canopies[candidate_id] = center_id

        if candidates :
            canopies[center_id] = center_id


    return canopies

def _createCanopies(field_inverted_index,
                    token_vector,
                    threshold,
                    field) :
                     
    logger.info("Canopy: %s", str(threshold) + field)
    canopy = makeCanopy(field_inverted_index, token_vector, threshold)


    return ((threshold, field),  canopy)

    

    
    
