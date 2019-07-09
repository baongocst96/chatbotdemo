## greet
* greet
   - utter_greet

## request_chung
* request_chung
   - utter_chung

## request vt
* request_vitri{"vi_tri":"*"}
    - action_vitri
	- action_restart

## request thongtin
* request_thongtin{"thong_tin":"*"}
	- action_thongtin
	- action_restart

## happy path
* request_restaurant
    - restaurant_form
    - form{"name": "restaurant_form"}
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries
    - action_restart

## unhappy path
* request_restaurant
    - restaurant_form
    - form{"name": "restaurant_form"}
* chitchat
    - utter_chitchat
    - restaurant_form
    - form{"name": null}
    - utter_slots_values
* thankyou
	- utter_greet
	- action_restart

## very unhappy path
* request_restaurant
    - restaurant_form
    - form{"name": "restaurant_form"}
* chitchat
    - utter_chitchat
    - restaurant_form
* chitchat
    - utter_chitchat
    - restaurant_form
* chitchat
    - utter_chitchat
    - restaurant_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries


##search hottel
* request_hottel
    - hottel_form
    - form{"name": "hottel_form"}
* chitchat
    - utter_chitchat
    - hottel_form
    - form{"name": null}    
    - utter_slots_values_ht
* affirm    
    - action_yes_sure
    - action_search_hottel
* deny 
    - action_no_sure
    - action_search_hottel    
* thankyou
    - utter_noworries
    - action_restart

##search perfect
* request_hottel
    - hottel_form
    - form{"name": "hottel_form"}
    - form{"name": null}    
    - utter_slots_values_ht
* affirm    
    - action_yes_sure
    - action_search_hottel
* deny 
    - action_no_sure
    - action_search_hottel    
* thankyou
    - utter_noworries
    - action_restart



   