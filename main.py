from airbnbsearchlist import get_accommodation_idxs
from airbnbdetail import extract_detail
#from airbnbdetail2 import extract_detail2

accommodation_idxs = get_accommodation_idxs()

extract_detail(accommodation_idxs)
#extract_detail2(accommodation_idxs)