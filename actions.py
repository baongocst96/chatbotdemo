# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, Restarted, AllSlotsReset
import mysql.connector



class HottelForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "hottel_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["lc_hottel", "num_room", "qu_hottel"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "lc_hottel": self.from_entity(entity="lc_hottel", intent="request_hottel"),
            "num_room":  self.from_entity(entity="num_room"),                      
            "qu_hottel": self.from_entity(entity="qu_hottel"),            
            
        }

    # USED FOR DOCS: do not rename without updating in docs
    @staticmethod
    def lc_hottel_db() -> List[Text]:
        """Database of supported lc_hottels"""

        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""

        try:
            int(string)
            return True
        except ValueError:
            return False

    # USED FOR DOCS: do not rename without updating in docs
    # def validate_qu_hottel(
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    #     )-> Optional[Text]:
    #     """Validate lc_hottel value."""
    #     return("qu_hottel", value)

    def validate_lc_hottel(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        """Validate lc_hottel value."""
        if(self.from_entity(entity="lc_hottel")):
            return{"lc_hottel": value}
        return {"lc_hottel": None}
        # else:
        # if value.lower() in self.lc_hottel_db():
        #     # validation succeeded, set the value of the "lc_hottel" slot to value
        #     return {"lc_hottel": value}
        # else:
        #     dispatcher.utter_template("utter_wrong_lc_hottel", tracker)
        #     # validation failed, set this slot to None, meaning the
        #     # user will be asked for the slot again
        #     return {"lc_hottel": None}

    def validate_num_room(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        """Validate num_room value."""
        return {"num_room": value}
        # if self.is_int(value) and int(value) > 0:
        #     return {"num_room": value}
        # else:
        #     dispatcher.utter_template("utter_wrong_num_room", tracker)
        #     # validation failed, set slot to None
        #     return {"num_room": None}
    
   
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        
        return []

class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "restaurant_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["cuisine", "num_people", "outdoor_seating", "preferences", "feedback"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "cuisine": self.from_entity(entity="cuisine", not_intent="chitchat"),
            "num_people": [
                self.from_entity(
                    entity="num_people", intent=["inform", "request_restaurant"]
                )
            ],
            "outdoor_seating": [
                self.from_entity(entity="seating"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "preferences": [
                self.from_intent(intent="deny", value="no additional preferences"),
                self.from_text(not_intent="affirm"),
            ],
            "feedback": [self.from_entity(entity="feedback"), self.from_text()],
        }

    # USED FOR DOCS: do not rename without updating in docs
    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisines"""

        return [
            "việt nam",
            "thái",
            "ấn độ",
            "trung quốc",
            "ý",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""

        try:
            int(string)
            return True
        except ValueError:
            return False

    # USED FOR DOCS: do not rename without updating in docs
    def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        """Validate cuisine value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": value}
        else:
            dispatcher.utter_template("utter_wrong_cuisine", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cuisine": None}

    def validate_num_people(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return {"num_people": value}
        else:
            dispatcher.utter_template("utter_wrong_num_people", tracker)
            # validation failed, set slot to None
            return {"num_people": None}

    def validate_outdoor_seating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Any:
        """Validate outdoor_seating value."""

        if isinstance(value, str):
            if "ngoài" in value:
                # convert "out..." to True
                return {"outdoor_seating": True}
            elif "trong" in value:
                # convert "in..." to False
                return {"outdoor_seating": False}
            else:
                dispatcher.utter_template("utter_wrong_outdoor_seating", tracker)
                # validation failed, set slot to None
                return {"outdoor_seating": None}

        else:
            # affirm/deny was picked up as T/F
            return {"outdoor_seating": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template("utter_submit", tracker)
        return []

class ActionCheckHottel(Action):
    def name(self) -> Text:
        return "action_search_hottel"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        lc_hottel = tracker.get_slot('lc_hottel')
        sure = tracker.get_slot('sure')
        if sure == "no":
            return [Restarted()]
        else:            
            sqlht = 'select name from chatbot where stt=1 '
            dispatcher.utter_template("utter_search_hottel", tracker, sqlht=sqlht)
            return []

class AcitonYes(Action):
    def name(self) -> Text:
        return "action_yes_sure"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return[SlotSet("sure","yes")]

class AcitonNo(Action):
    def name(self) -> Text:
        return "action_no_sure"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return[SlotSet("sure","no")]

class ActionRestart(Action):
    def name(self)-> Text:
        return "action_restart"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return[Restarted()]

class ViTri(Action):
    def name(self) -> Text:
        return "action_vitri"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        dict_vitri={"bến ninh kiều":"Nằm ở: 38 Hai Bà Trưng, ​​Tân An, Ninh Kiều, Cần Thơ",
                    "chợ nổi cái răng":"Nằm ở: 46 Hai Bà Trưng, Lê Bình, Cái Răng, Cần Thơ",
                    "nhà cổ bình thuỷ":"Nằm ở: 144 Bùi Hữu Nghĩa, Bình Thuỷ, Bình Thủy, Cần Thơ, Việt Nam",
                    "chùa ông":"Nằm ở: 32, Hai Bà Trưng, Tân An, Ninh Kiều, Cần Thơ, Việt Nam",
                    "vườn cây mỹ khánh":"Nằm ở: Mỹ Khánh, Phong Điền, Cần Thơ, Việt Nam",
                    "chợ đêm":"Nằm ở: Hai Bà Trưng, Tân An, Ninh Kiều, Cần Thơ, Việt Nam"
                    }
        if any(tracker.get_latest_entity_values("vi_tri")):
            # entity was picked up, validate slot
            vitri = tracker.get_slot("vi_tri")
            ask = dict_vitri[vitri]
            dispatcher.utter_template("utter_vitri", tracker, vi_tri=vitri, tt_vitri=ask)
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_vitri", tracker)
        return []
class ViTri(Action):
    def name(self) -> Text:
        return "action_thongtin"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        dict_thongtin={"bến ninh kiều":"Theo Wiki: Bến Ninh Kiều là một địa danh du lịch có từ lâu và hấp dẫn du khách bởi phong cảnh sông nước hữu tình và vị trí thuận lợi nhìn ra dòng sông Hậu. Từ lâu bến Ninh Kiều đã trở thành biểu tượng về nét đẹp thơ mộng bên bờ sông Hậu của cả Thành phố Cần Thơ, thu hút nhiều du khách đến tham quan và đi vào thơ ca.",
                    "chợ nổi cái răng":"Theo Wiki: Chợ nổi Cái Răng là chợ nổi chuyên trao đổi, mua bán nông sản, các loại trái cây, hàng hóa, thực phẩm, ăn uống ở trên sông và là điểm tham quan đặc sắc của quận Cái Răng, thành phố Cần Thơ",
                    "nhà cổ bình thuỷ":"Bằng giá trị kiến trúc, lịch sử của mình, nhà cổ Bình Thủy đã được công nhận là “di tích nghệ thuật cấp quốc gia”, ngày càng thu hút nhiều khách đến thăm cũng như các đoàn làm phim về mượn bối cảnh cho những thước phim của mình.",
                    "chùa ông":"Theo Wiki: Chùa Ông (Cần Thơ), tên gốc là Quảng Triệu Hội Quán (chữ Hán: 廣肇會館；广肇会馆). Đây là một ngôi chùa của người Hoa gốc Quảng Đông tại Cần Thơ, và là một di tích lịch sử cấp quốc gia kể từ năm 1993.",
                    "vườn cây mỹ khánh":"Đặt chân tới vườn trái cây này thì bạn sẽ được tham quan hơn 20 giống cây trồng khác nhau sẽ cho bạn một trải nghiệm đặc biệt.",
                    "chợ đêm":"Ở đây có bán rất nhiều món ngon, trong đó có những món đặc trưng của miền Tây mà tiêu biểu là những món chè"
                    }
        if any(tracker.get_latest_entity_values("thong_tin")):
            # entity was picked up, validate slot
            thongtin = tracker.get_slot("thong_tin")
            ask = dict_thongtin[thongtin]
            dispatcher.utter_template("utter_thongtin", tracker, thong_tin=thongtin, tt_thongtin=ask)
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_thongtin", tracker)
        return []

class ActionTestDB(Action):
    def name(self)-> Text:
        return "action_test"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:      
    
        mydb = mysql.connector.connect(
           host="localhost",
           user="root",
           passwd="abcd1234",
           database="rasa",
           auth_plugin='mysql_native_password'
         )
        sqlht = 'select name from chatbot'
        mycursor = mydb.cursor()
        mycursor.execute(sqlht)
        myresult = mycursor.fetchall()  
        for x in myresult:
            dispatcher.utter_template("utter_test", tracker, test=x)
        return[]

class ActionUpdateLC(Action):
    def name(self)-> Text:
        return "action_update_ht"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if any(tracker.get_latest_entity_values("lc_hottel")):
            lc_hottel = get_latest_entity_values("lc_hottel")
            return[SlotSet("lc_hottel", lc_hottel)]

class ActionUpdateRom(Action):
    def name(self)-> Text:
        return "action_update_room"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if any(tracker.get_latest_entity_values("num_room")):
            lc_hottel = get_latest_entity_values("num_room")
            return[SlotSet("num_room", num_room)]

class ActionUpdateQu(Action):
    def name(self)-> Text:
        return "action_update_quaht"

    def run(self,
       dispatcher: CollectingDispatcher,
       tracker: Tracker,
       domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if any(tracker.get_latest_entity_values("qu_hottel")):
            lc_hottel = get_latest_entity_values("qu_hottel")
            return[SlotSet("qu_hottel", num_room)]