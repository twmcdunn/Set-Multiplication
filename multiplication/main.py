
## get all sets of a given cardinality
#1. recursively get all sets of next smallest cardinality
#2. for each note 0 - 11, if not contained in the smaller set, create a copy of the smaller set with that note appended
# this actually returns all combinations of N pitch-classes, not all unique sets of a given cardinality
def all_sets(card, set = []):
    if len(set) == card:
        set.sort()
        return [set]
    compSets = []
    highestNote = 0
    if len(set) > 0:
        max(set)
    for i in range(highestNote, 12):
        if i not in set:
            set_copy = set.copy()
            set_copy.append(i)
            compSets.extend(all_sets(card, set_copy))
    return compSets

print(all_sets(3))

#put set into normal order
def normal_order(set):
    bestOrds = get_all_rotations(set)
    while True:
        for interval in range(len(set)):
            best = 1000 # dummy value
            for s in bestOrds:
                i = s[len(set) - 1 - interval] - s[0]
                if i < 0:
                    i += 12
                best = min(best, i)
            bestOrdsNarrowed = []
            for s in bestOrds:
                i = s[len(set) - 1 - interval] - s[0]
                if i < 0:
                    i += 12
                if i == best and s not in bestOrdsNarrowed:#not really necessary anymore since rotations takes out transpositionally symmetrical redundancies
                    bestOrdsNarrowed.append(s)
            bestOrds = bestOrdsNarrowed
        if len(bestOrds) == 1:
            return bestOrds[0]
        
        
def transToZero(set):
    transSet = []
    for i in range(len(set)):
        transSet.append((set[i] + 12 - set[0]) % 12)
    return transSet

#once we have all combinations of N pitch-classes, we need to narrow it down to the unique sets
#sets are unique if they aren't related to eachother be transposition, i.e they have a unique prime
#form in solomen's system.  (We're not worried about inversional equivalence)
def uniqueSets(card):
    allSets = all_sets(card)
    uniqueSets = []
    for set in allSets:
        s = normal_order(set)
        if s not in uniqueSets:
            uniqueSets.append(s)
    return uniqueSets

def isCompProd(set1, set2):
    prod = []
    for i in range(len(set1)):
        for n in range(len(set2)):
            sum = (set1[i] + set2[n]) % 12
            if sum not in prod:
                prod.append(sum)
            else:
                return False
    return True

# returns every mulptiplaction that can be performed (doesn't actually do the multiplying)
# eg. each member of  
def allMultiples(seta, setb, mult = []):
    if len(mult) == len(seta):
        return [mult]
    mult1 = mult.copy()
    mult1.append(seta)
    options1 = allMultiples(seta,setb,mult1)
    mult2 = mult.copy()
    mult2.append(setb)
    options2 = allMultiples(seta,setb,mult2)
    options1.extend(options2)
    return options1

#print(allMultiples([2,3,4],[0,1]))



def canFormAgg(seta, setb, allowReps = False, superSet = range(12)):
    superSet = normal_order(superSet)
    set1 = seta

    allMult = allMultiples(seta,setb)
    workingMults = []
    for mult in allMult:
        prod = []
        reps = False
        for i in range(len(set1)):
            set2 = mult[i]
            for n in range(len(set2)):
                sum = (set1[i] + set2[n]) % 12
                if sum not in prod:
                    prod.append(sum)
                else:
                    reps = True
        prod.sort()
        prod = normal_order(prod)
        #if len(prod) == 12:
            #print("agg")
        if  prod == superSet and (not reps or allowReps):
            workingMults.append(mult)
    for mult in workingMults:
        mult.insert(0,seta)
    return workingMults

def get_all_rotations(set):
    rotations = []
    for first in range(len(set)):
        rot = []
        for i in range(len(set)):
            rot.append(set[(first + i) % len(set)])
        rot = transToZero(rot)
        if rot not in rotations:
            rotations.append(rot)
    return rotations


card4Sets = uniqueSets(4)
card3Sets = uniqueSets(3)
pairs = []
for card4Set in card4Sets:
    for card3Set in card3Sets:
        if(isCompProd(card4Set,card3Set)):
            pairs.append([card3Set,card4Set])

for p in pairs:
    print(p)

print()

pairs = []

#sets = []
#for card in range(3,5):
 #   sets.extend(uniqueSets(card))

for setA in card4Sets:
    rotationsA = get_all_rotations(setA)
    for ra in rotationsA:
        for setB in card4Sets:
            rotationsB = get_all_rotations(setB)
            for rb in rotationsB:
                pairs1 = canFormAgg(ra,rb, True, [0,1,3,4,6,7,9,10])##must be 'communicative'
                pairs2 = canFormAgg(rb,ra, True, [0,1,3,4,6,7,9,10])
                if len(pairs1) > 0 and len(pairs2) > 0:
                    pairs.extend(pairs1)
                    pairs.extend(pairs2)


#pairs.extend(canFormAgg([0,4,8],[0,4,6,7],True, [0,1,3,4,6,7,9,10]))
outfile = open('results.txt', 'w')

for p in pairs:
    print(p)
    outfile.write(str(p) + '\n')

outfile.close()



