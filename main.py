from airbnbsearchlist import get_accommodation_infos
from airbnbdetail import extract_detail
#from airbnbdetail2 import extract_detail2

accommodation_infos = get_accommodation_infos()

extract_detail(accommodation_infos)
#extract_detail2(accommodation_idxs)