from unicodeMagic import UnicodeReader

filename = r"C:\Users\tickc\OneDrive\Documents\GitHub\gender\data\nam_dict.txt"
f = open(filename, 'rb')

reader = UnicodeReader(f)

genderDict = {}

idx = 0

shortNames = []   
 
#Create Dictionary of names 

for row in reader:
    if idx > 361: #Names start after the 361st line
        text = row[0]
        mf = text[:2].strip() # M,1M,?M, F,1F,?F, ?, =
        #  =  <short_name> <long_name> 
        name = text[2:29].lower().strip()
        sortingFlag = text[29] # +,-; ignore +
        frequencies = text[30:-2]
    
        if sortingFlag != '+':
            if mf == '=':
                shortNames.append([name, frequencies])
            else:
                '''"Jun+Wei" represents the names "Jun-Wei", "Jun Wei" and "Junwei"'''
                if name.find('+') != -1:
                    names = [name.replace('+','-'), name.replace('+',' '), name.replace('+','').capitalize()]
                else:
                    names = [name]
                for name in names:
                    if genderDict.has_key(name):
                        genderDict[name].append([mf, frequencies])
                    else:
                        genderDict[name] = [[mf, frequencies]]
    idx += 1
             