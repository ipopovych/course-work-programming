import pandas as pd
import os                                                                                                             


def dict_datafiles(dir):
    r = {}
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = next(os.walk(subdir))[2]
        if (len(files) > 0):                                                                                          
            for file in files:
                if file == 'documents.csv':
                    r[int(subdir[-4:])] = subdir + "/" + file
    return r


class Cleaner:
    def __init__(self, paramfile):
        """paramfile: txt file with codes to save"""
        codes = []
        with open(paramfile, encoding='utf-8') as f:
            for line in f:
                codes.append(int(line.strip().split()[0]))
        self.codes = codes

    def clear(self, filename):
        """filename: file with court data"""
        df = pd.read_csv(filename, delimiter="\t")

        # clearing from judjements without code
        clear_df = df[~df["category_code"].isnull()]

        # rewriting codes as integers
        clear_df["category_code"].astype('int', inplace=True)
        ndf = pd.DataFrame()
        for code in self.codes:
            ndf = ndf.append(clear_df[clear_df["category_code"] == code])
            ndf = ndf[ndf['judgment_code'] == 1]
        return ndf


# myfiles = dict_datafiles(os.curdir)
# # print(myfiles)
# cleaner = Cleaner('military.txt')
# military_dt = {}
# for k, v in myfiles.items():
#     military_dt[k] = cleaner.clear(v)
#     print('len of cleared', len(military_dt[k]))
#     military_dt[k].to_csv(str(k) + '-1-cleared.csv')

