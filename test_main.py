from main import str_to_bool,roll_random_in_array,unpack_keys
import sys
import pytest
from utils import psudo_list_rng

def test_str_to_bool():
    assert str_to_bool('True') == True
    assert str_to_bool('False') == False
    with pytest.raises(SystemExit):    
        assert str_to_bool('') == sys.exit("invalid debug asisgnment in .env")

def test_rng():
    scared_responses = ['Please stop yelling at me its scawwy but ','Loud Noises scawwy but ','AAAHH but ']
    un_scared_response = ['Thankies and ','thankuus ']
    #array size is so small it always returns 0 when seeded for tests
    assert roll_random_in_array(scared_responses,1) == 'Please stop yelling at me its scawwy but '

def test_unpack_keys():
    bot_talk_keywords = {'hello':'hw','hey gura what do you think of ':'rng_like','source me':'source'    }
    assert unpack_keys(bot_talk_keywords) == ['hello','hey gura what do you think of ','source me']

def test_psudo_rng():
    startup_statuses = ['crying over RNG','with the dev console','crashing this bot with no error logs','gao']
    assert psudo_list_rng(startup_statuses, 'crying over RNG') == ['with the dev console','crashing this bot with no error logs','gao']
    assert psudo_list_rng(startup_statuses, 'with the dev console') == ['crying over RNG','crashing this bot with no error logs','gao']
