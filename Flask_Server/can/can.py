import json

class Can:
    can_data = {}
    idx = None

    def __init__(self):
        self.idx = -1

    def set_data(self, can_data):
        self.idx += 1
        self.can_data[self.idx] = self.parse(can_data)
        return self.idx

    def get_data(self, idx):
        return self.can_data.get(idx, None)

    def get_idx(self):
        return self.idx

    def parse(self, can_data):
        d_list = []
        for data in can_data.split("\n"):
            if not data:
                continue
            d = {}
            data = data.split('    ')
            data.pop(1)
            d['Timestamp'] = data[0].split(' ')[-1]
            d['ID'] = data[1].split(' ')[-1]
            d['RTR'] = data[2]
            d['DLC'] = data[3].split(' ')[-1]
            d['Offset'] = data[4]
            d['Detect'] = data[5]
            d_list.append(d)
        return d_list

#Debug Code
'''
if __name__ == "__main__":
    d = 'Timestamp: 1479109287.406775        ID: 0165    000    DLC: 8    08 f8 7f 00 00 00 04 8b\n' * 10
        d = '1479109287.296843        ID: 0165    000    DLC: 8    08 f8 7f 00 00 00 09 86'
    can = Can()
    can.set_data(d)
    print can.get_data(can.get_idx())
'''
