import sys,re

white_data= {
    '0110' : {'re': [8, '( [0-f]0)( [0-f]c)( [0-f]0) [0-f](1|3|5|7|9|b|d|f)( [0-f]0)( 00){3}'], 'avg': 0.1, 'bound': 0.001} ,
    '0034' : {'re': [8, '( 00){8}'], 'avg': 1.0, 'bound': 0.001} ,
    '0050' : {'re': [4, '( 00)( [0-f]{2}){2}( 00)'], 'avg': 0.2, 'bound': 0.001} ,
    '0018' : {'re': [8, ' [0-f]{2} 00( [0-f]{2}){6}'], 'avg': 0.2, 'bound': 0.001} ,
    '0690' : {'re': [8, '( [0-f]{2}){5} [0-f]0 [0-f](1|3|5|7|9|b|d|f) [0-f](0|4|8|c)'], 'avg': 0.1, 'bound': 0.005} ,
    '051a' : {'re': [8, ' 00 [0-f]{2}( 00){6}'], 'avg': 0.2, 'bound': 0.005} ,
    '04b0' : {'re': [8, '( [0-f]{2}){8}'], 'avg': None, 'bound': None} ,
    '04b1' : {'re': [8, '( [0-f]{2}){4}( 00){3}( [0-f]{2})'], 'avg': None, 'bound': None} ,
    '0545' : {'re': [8, '( [0-f]{2}){2} 00( [0-f]{2}){5}'], 'avg': 0.01, 'bound': 0.005} ,
    '0510' : {'re': [8, '( 00){2} [0-f]0 00( [0-f]{2}){2}( 00){2}'], 'avg': 0.1, 'bound': 0.003} ,
    '059b' : {'re': [8, ' 00 [0-f]{2}( 00){5} [0-f](0|4|8|c)'], 'avg': 0.1, 'bound': 0.005} ,
    '04f2' : {'re': [8, '( [0-f]{2}){2} [0-f](0|2|4|6|8|a|c|e) 38( 00){3} [0-f]{2}'], 'avg': 0.02, 'bound': 0.006} ,
    '04f0' : {'re': [8, ' 00 [0-f]{2} [0-f](0|2|4|6|8|a|c|e)( 00){2}( [0-f]{2}){3}'], 'avg': 0.02, 'bound': 0.006} ,
    '04f1' : {'re': [8, '( [0-f]{2}){3}( 00){5}'], 'avg': 0.1, 'bound': 0.005} ,
    '0329' : {'re': [8, ' (0f|40|85|d7)( [0-f]{2}){6} 10'], 'avg': 0.01, 'bound': 0.004} ,
    '05f0' : {'re': [2, '( 00){2}'], 'avg': 0.2, 'bound': 0.005} ,
    '0370' : {'re': [8, ' ff [0-f]{2} [0-f]0 [0-f]{2} ff( 00){2} [0-f](0|4|8|c)'], 'avg': 0.01, 'bound': 0.004} ,
    '0587' : {'re': [8, '( 00){7} 0[0-e]'], 'avg': 0.1, 'bound': 0.004} ,
    '02b0' : {'re': [5, '( [0-f]{2}){3} 07( [0-f]{2})'], 'avg': 0.01, 'bound': 0.004} ,
    '01f1' : {'re': [8, ' 00( [0-f]{2}){2}( [0-f]0)( [0-f]{2}){2}( [0-f]0)( [0-f]{2})'], 'avg': None, 'bound': None} ,
    '0080' : {'re': [8, '( [0-f]{2}) 17( [0-f]{2}){2}'], 'avg': 0.01, 'bound': 0.002} ,
    '0081' : {'re': [8, '( [0-f]{2}){3}( 00){4}( [0-f]{2})'], 'avg': 0.01, 'bound': 0.002} ,
    '043f' : {'re': [8, '( [0-f]{2}){2} 60( [0-f]{2}){2} [0-f](0|4|8|c) [0-f]{2} 00'], 'avg': 0.01, 'bound': 0.005} ,
    '00a0' : {'re': [8, '( [0-f]{2}){2} [0-f](0|2|4|6|8|a|c|e)( [0-f]{2}){3}( 00)( [0-f]{2})'], 'avg': 0.1, 'bound': 0.011} ,
    '0260' : {'re': [8, '( [0-f]{2}){3}( 30 ff)( [0-f]{2}){3}'], 'avg': 0.01, 'bound': 0.004} ,
    '0382' : {'re': [8, ' 40 fe 0f( 00){4} 0(0|4|8|c)'], 'avg': 0.02, 'bound': 0.004} ,
    '0120' : {'re': [4, '( 00){4}'], 'avg': 0.2, 'bound': 0.001} ,
    '0220' : {'re': [8, '( [0-f]{2}){8}'], 'avg': None, 'bound': None} ,
    '0042' : {'re': [8, '( [0-f]{2}){2}( ff){2}( 00){4}'], 'avg': 1.0, 'bound': 0.001} ,
    '0043' : {'re': [8, '( [0-f]{2})( 00){6}( [0-f]{2})'], 'avg': 1.0, 'bound': 0.001} ,
    '0044' : {'re': [8, '( 00){3}( [0-f]{2}){2}( 00){3}'], 'avg': 1.0, 'bound': 0.001} ,
    '0165' : {'re': [8, '( [0-f]{2}){4}( 00){2}( 0[0-f])( [0-f]{2})'], 'avg': 0.01, 'bound': 0.002} ,
    '0164' : {'re': [8, ' 00 08( 00){4}( 0[0-f]){2}'], 'avg': None, 'bound': None} ,
    '05a2' : {'re': [4, ' [0-f]{2} 00 a5 01'], 'avg': None, 'bound': None} ,
    '05a0' : {'re': [8, '( 00){8}'], 'avg': None, 'bound': None} ,
    '0350' : {'re': [8, '( [0-f]{2}){2}( [0-f]4)( [0-f]{2}){2}( 00){2}( [0-f]{2})'], 'avg': 0.02, 'bound': 0.004} ,
    '02a0' : {'re': [8, '( [0-f]{2})( 00)( [0-f]{2}){6}'], 'avg': 0.01, 'bound': 0.004} ,
    '0440' : {'re': [8, ' ff( [0-f]{2}){2} 00 ff [0-f](0|4|8|c)( [0-f]{2}){2}'], 'avg': 0.01, 'bound': 0.005} ,
    '05e4' : {'re': [3, ' 00 [0-f]{2} 00'], 'avg': 0.1, 'bound': 0.005} ,
    '018f' : {'re': [8, '( [0-f]{2}){3}( 00){2}( [0-f]{2})( [0-f]0){2}'], 'avg': 0.01, 'bound': 0.003} ,
    '0153' : {'re': [8, ' 00 80 10 ff 00 ff ([0-f]0) ([0-f]e)'], 'avg': None, 'bound': None} ,
    '00a1' : {'re': [8, '( [0-f]{2}){2}( 80){2}( [0-f]{2})( 00){3}'], 'avg': 0.1, 'bound': 0.011} ,
    '0517' : {'re': [8, ' [0-f]{2}( 00){7}'], 'avg': 0.2, 'bound': 0.003} ,
    '0316' : {'re': [8, '( [0-f]{2}){7} 7f'], 'avg': 0.01, 'bound': 0.005} ,
    '02c0' : {'re': [8, ' [0-f]{2}( 00){7}'], 'avg': None, 'bound': None}
}
previous_dict = dict()


class detectCan():
    global previous_dict, white_data

    def check_offset(self, line):
        can_id = line.split()[3]
        dlc = line.split()[6]
        regex = "ID: " + can_id + "\s{4}000\s{4}DLC: " + dlc + "\s{3}"

        attack_type = 'Fuzzy'

        if can_id in white_data:
            if dlc == str(white_data[can_id]['re'][0]):
                regex += white_data[can_id]['re'][1]

                if self.is_match(regex,line):
                    attack_type = 'Normal'
        return attack_type

    def is_match(self, regex, text):
        match = re.search(regex, text)
        return match is not None

    def check_interval(self, line):
        can_id = line.split()[3]
        time_stamp = float(line.split()[1])
        attack_type = 'Fuzzy'

        if can_id in white_data:
            if white_data[can_id]['avg'] == None :
                attack_type = 'Normal'
            else:
                if not can_id in previous_dict.keys():
                    previous_dict[can_id] = time_stamp
                    attack_type = 'Normal'
                else:
                    temp_interval = time_stamp - previous_dict[can_id]
                    if temp_interval < white_data[can_id]['avg'] + white_data[can_id]['bound'] and temp_interval > white_data[can_id]['avg'] - white_data[can_id]['bound']:
                        attack_type = 'Normal'
                    previous_dict[can_id] = time_stamp

        return attack_type

    def final_check(self, line):
        can_id = line.split()[3]
        dlc = line.split()[6]
        regex = "ID: " + can_id + "\s{4}000\s{4}DLC: " + dlc + "\s{3}"
        attack_type = 'Fuzzy'
        if dlc == '8' and can_id == '0000':
            regex += "( 00){8}"
            if self.is_match(regex,line):
                attack_type = 'Dos'

        else:
            result_offset = self.check_offset(line)
            result_interval = self.check_interval(line)

            if result_offset == 'Normal' and result_interval == 'Normal':
                attack_type = 'Normal'

            #for debug
            #if result_offset == 'F' and result_interval == 'N':
            #    print line

        line = line + "    " + attack_type
        return line


    def start_Detact(self, line):
        return self.final_check(line)
