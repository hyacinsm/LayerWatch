class data_wrapper:
    
    # parameters passed
    CADENCE = 'cadence'
    STATUS = 'status'
    TIME = 'time'
    IMG = 'img'
    BTN_TXT = 'btn_txt'
    
    
        
    def __init__(self, cadence, status, time, img, btn_txt):
        self.usr_cadence = str(cadence)
        self.usr_status = status
        self.usr_time = time
        self.usr_img  = img
        self.usr_btn_txt = btn_txt
        
    def gen_dict(self):
        return {
            self.CADENCE : self.usr_cadence,
            self.STATUS : self.usr_status,
            self.TIME : self.usr_time,
            self.IMG : self.usr_img,
            self.BTN_TXT: self.usr_btn_txt
        }

