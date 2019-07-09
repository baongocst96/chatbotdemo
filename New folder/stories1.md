##hello
* greet
	- utter_greet
	- action_restart

##thankyou
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
    - action_restart

##search unperfect
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

##search hottel
* request_hottel
    - hottel_form
    - form{"name": "hottel_form"}
* update_hottel
    - action_update_ht
    - utter_update_ht
    - hottel_form
    - form{"name": null}    
    - utter_slots_values_ht
* affirm
    - action_test    
    - action_yes_sure
    - action_search_hottel    
* thankyou
    - utter_noworries
    - action_restart  




