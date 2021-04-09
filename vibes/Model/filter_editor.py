from casus.filter_editor.editors import *
import math

class filter_editor():
    def __init__(self):
        """
        :param first: -> int > premiere donne de temps
        :param last: -> int > derniere donnee de temps
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.type = "filter_editor"
    def __call__(self, data_in, data_out,fc1,fc2,type):
        self.data_in = data_in
        fourier_no_complex = [0] * len(self.data_in[0].fourier_complete)
        for x in range(0, len(self.data_in[0].fourier_complete)):
            fourier_no_complex[x] = self.data_in[0].fourier_complete[x].real
        self.data_out = data_out
        self.vout = data_out[0].fourier_no_complexe
        self.freq = data_out[0].freq
        self.freq_complete = data_out[0].freq_complete

        self.vin = fourier_no_complex
        self.vin_positive = data_in[0].fourier_no_complexe_positive
        self.vout_positive = data_out[0].fourier_no_complexe_positive
        self.fc1 = fc1
        self.fc2 = fc2
        self.type = type

        self.phaseShift = 0;
    def set_data_for_graphic(self):

            self.impulsion_db_positive = [0] * len(self.vin_positive)
            self.impulsion_db = [0] * len(self.vin)
            answer = 0
            for x in range(0, len(self.vin)):
                if (self.vout[x] / self.vin[x] < 0.0000000000001):
                    answer = 0.00000000000001
                else:
                    answer = self.vout[x] / self.vin[x]

                if (self.freq_complete[x] >= 0):
                    self.impulsion_db_positive[x] = 20 * math.log(answer)
                    self.impulsion_db[x] = 20 * math.log(answer)
                else:
                    self.impulsion_db[x] = 20 * math.log(answer)

class filter_editor_bode():

    def __init__(self):
        self.name = "filter_editor_bode"

    def __call__(self, data):
        self.data_in = data[0].data_in
        self.data_out = data[0].data_out
        self.vout = data[0].vout
        self.freq = data[0].freq
        self.freq_complete = data[0].freq_complete

        self.vin = data[0].vin
        self.vin_positive = data[0].vin_positive
        self.vout_positive = data[0].vout_positive
        self.fc1 = data[0].fc1
        self.fc2 = data[0].fc2
        self.type = data[0].type

    def get_data_for_graphic(self):

        self.impulsion_db_positive = [0]*len(self.vin_positive)
        self.impulsion_db = [0]*len(self.vin)
        answer = 0
        for x in range(0,len(self.vin)):
            if(self.vout[x]/self.vin[x] < 0.0000000000001):
                answer = 0.00000000000001
            else:
                answer = self.vout[x] / self.vin[x]

            if(self.freq_complete[x] >= 0):
                self.impulsion_db_positive[x] = 20 * math.log(answer)
                self.impulsion_db[x] = 20 * math.log(answer)
            else:
                self.impulsion_db[x] = 20* math.log(answer)

    def modify_response(self, first, last, attenuation, type):

        if(type == "passe bas"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] <= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] >= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20) )* self.vin[x]

        if(type == "passe haut"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] >= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] <= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20))* self.vin[x]
        if(type == "passe bande"):
            for x in range(len(self.freq_complete)):
                if (self.freq_complete[x] < 0):
                    if (self.freq_complete[x] >= -1 * float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x]< -1 * float(last)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                elif (self.freq_complete[x] >= 0):
                    if (self.freq_complete[x] <= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x] > float(last)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]

class filter_editor_phase():

    def __init__(self):
        self.name = "filter_editor_phase"

    def __call__(self, data):
        self.data_in = data[0].data_in
        self.data_out = data[0].data_out
        self.vout = data[0].vout
        self.freq = data[0].freq
        self.freq_complete = data[0].freq_complete

        self.vin = data[0].vin
        self.vin_positive = data[0].vin_positive
        self.vout_positive = data[0].vout_positive
        self.fc1 = data[0].fc1
        self.fc2 = data[0].fc2
        self.type = data[0].type

    def get_data_for_graphic(self):

        self.constant = 1/(self.fc1 * math.pi *2)
        self.impulsion_db_positive = [0]*len(self.freq)
        self.impulsion_db = [0]*len(self.freq_complete)


        if(self.name == "filter_editor_phase"):
            for x in range(0,len(self.impulsion_db)):
                if(self.freq_complete[x] >= 0):
                    self.impulsion_db_positive[x] = -1* math.atan(self.constant*self.freq_complete[x]*math.pi*2)
                    self.impulsion_db[x] = -1* math.atan(self.constant*self.freq_complete[x]*math.pi*2)
                else:
                    self.impulsion_db[x] = -1* math.atan(self.constant*self.freq_complete[x]*math.pi*2)

        elif (self.name == "passe bas"):
            for x in range(len(self.freq_complete)):
                if (self.freq_complete[x] >= 0):
                    if (self.freq_complete[x] > self.fc1):
                        self.impulsion_db_positive[x] = float(self.phaseShift);
                        self.impulsion_db[x] = float(self.phaseShift);
                    else:
                        self.impulsion_db_positive[x] = -1 * math.atan(
                            self.constant * self.freq_complete[x] * math.pi * 2)
                        self.impulsion_db[x] = -1 * math.atan(self.constant * self.freq_complete[x] * math.pi * 2)
                else:
                    if (self.freq_complete[x] <= -1 * self.fc1):
                        self.impulsion_db[x] = float(self.phaseShift);
                    else:
                        self.impulsion_db[x] = -1 * math.atan(self.constant * self.freq_complete[x] * math.pi * 2)

        elif (self.name == "passe haut"):
            for x in range(len(self.freq_complete)):
                if (self.freq_complete[x] >= 0):
                    if (self.freq_complete[x] < self.fc1):
                        self.impulsion_db_positive[x] = float(self.phaseShift);
                        self.impulsion_db[x] = float(self.phaseShift);
                    else:
                        self.impulsion_db_positive[x] = -1 * math.atan(self.constant * self.freq_complete[x] * math.pi * 2)
                        self.impulsion_db[x] = -1 * math.atan(self.constant * self.freq_complete[x] * math.pi * 2)
                else:
                    if (self.freq_complete[x] >= -1 * self.fc1):
                        self.impulsion_db[x] = float(self.phaseShift);
                    else:
                        self.impulsion_db[x] = -1 * math.atan(self.constant * self.freq_complete[x] * math.pi * 2)

        elif (self.name == "passe bande"):
            for x in range(len(self.freq_complete)):
                for x in range(len(self.freq_complete)):
                    if (self.freq_complete[x] >= 0):
                        if (self.freq_complete[x] <= self.fc1):
                            self.impulsion_db_positive[x] = float(self.phaseShift);
                            self.impulsion_db[x] = float(self.phaseShift);
                        elif(self.freq_complete[x] > self.fc2):
                            self.impulsion_db_positive[x] = float(self.phaseShift);
                            self.impulsion_db[x] = float(self.phaseShift);
                        else:
                            self.impulsion_db_positive[x] = -1 * math.atan(
                                self.constant * self.freq_complete[x] * math.pi * 2)
                            self.impulsion_db[x] = -1 * math.atan(
                                self.constant * self.freq_complete[x] * math.pi * 2)
                    else:
                        if (self.freq_complete[x] >= -1 * self.fc1):
                            self.impulsion_db[x] = float(self.phaseShift);
                        elif (self.freq_complete[x] < -1 * self.fc2):
                            self.impulsion_db[x] = float(self.phaseShift);
                        else:
                            self.impulsion_db[x] = -1 * math.atan(
                                self.constant * self.freq_complete[x] * math.pi * 2)

    def modify_response(self, first, last, attenuation, type):
        self.name = type
        self.phaseShift =attenuation
        if(type == "passe bas"):
            self.fc1 = float(first)
        if(type == "passe haut"):
            self.fc1 = float(first)
        if(type == "passe bande"):
            self.fc1 = float(first)
            self.fc2 = float(last)

class filter_editor_pole():

    def __init__(self):
        self.type = "filter_editor_bode"

    def __call__(self, data):
        self.data_in = data[0].data_in
        self.data_out = data[0].data_out
        self.vout = data[0].vout
        self.freq = data[0].freq
        self.freq_complete = data[0].freq_complete

        self.vin = data[0].vin
        self.vin_positive = data[0].vin_positive
        self.vout_positive = data[0].vout_positive

    def get_data_for_graphic(self):

        self.impulsion_db_positive = [0]*len(self.vin_positive)
        self.impulsion_db = [0]*len(self.vin)
        answer = 0
        for x in range(0,len(self.vin)):
            if(self.vout[x]/self.vin[x] < 0.0000000000001):
                answer = 0.00000000000001
            else:
                answer = self.vout[x] / self.vin[x]

            if(self.freq_complete[x] >= 0):
                self.impulsion_db_positive[x] = 20 * math.log(answer)
                self.impulsion_db[x] = 20 * math.log(answer)
            else:
                self.impulsion_db[x] = 20* math.log(answer)

    def modify_response(self, first, last, attenuation, type):

        if(type == "passe bas"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] <= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] >= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20) )* self.vin[x]

        if(type == "passe haut"):
            for x in range(len(self.freq_complete)):
                if(self.freq_complete[x] < 0):
                    if(self.freq_complete[x] >= -1* float(first)):
                        self.vout[x] = math.pow(10,(float(attenuation)/20)) *self.vin[x]
                if(self.freq_complete[x] >=0):
                    if(self.freq_complete[x] <= float(first)):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20) )* self.vin[x]
        if(type == "passe bande"):
            for x in range(len(self.freq_complete)):
                if (self.freq_complete[x] < 0):
                    if (self.freq_complete[x] > -1 * self.cut_off* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x]< -1 * self.cut_off2* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                elif (self.freq_complete[x] >= 0):
                    if (self.freq_complete[x] < self.cut_off* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]
                    elif (self.freq_complete[x] > self.cut_off2* 2):
                        self.vout[x] = math.pow(10, (float(attenuation) / 20)) * self.vin[x]




