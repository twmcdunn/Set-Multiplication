

def all_possible_chords(chord = []):
    # if the input is already 3 notes, you're done!
    if len(chord) == 3: 
        chord.sort()
        return [chord]
    
    # an array to hold the 'completed chords'
    # (3 note chords)
    compchords = []

    # get the highest note in the input chord
    highestNote = -1
    if len(chord) > 0:
        highestNote = max(chord)

    #go up the chromatic scale, starting just 
    # above the highest note in the input chord
    for i in range(highestNote + 1, 12):
        # if the note in question isn't in the chord
        # make a copy of the chord with this note added
        # pass the copy as input to this function itself
        # add the results of this to the completed chords array
        if i not in chord:
            chord_copy = chord.copy()
            chord_copy.append(i)
            compchords.extend(all_possible_chords(chord_copy))
    return compchords

print(all_possible_chords())

def all_possible_chord_progressions(chord_a, chord_b, progression = []):
    # if the length of the progression is equal to the
    # number of notes in the chord you're multiplying out
    # then you're done!
    if len(progression) == len(chord_a):
        return [progression]
    
    #an array to hold the results
    allPossibleProgressions = []
    
    # create a copy of the progression, adding chord A as the
    # next chord. (It needs to be transposed so it's root is the
    # next note in the chord.)
    option1 = progression.copy()
    option1.append(transpose(chord_a, chord_a[len(progression)]))

    # pass this progression as input and find all possible progressions
    # for the remaining chord members
    allPossibleProgressions = all_possible_chord_progressions(chord_a,chord_b,option1)

    # do the same thing as above, but assigning chord B as the
    # next chord in the progression
    option2 = progression.copy()
    option2.append(transpose(chord_b, chord_a[len(progression)]))
    allPossibleProgressions.extend(all_possible_chord_progressions(chord_a,chord_b,option2))

    return allPossibleProgressions


def transpose(chord, interval):
    return None