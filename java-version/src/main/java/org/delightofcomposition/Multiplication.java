package org.delightofcomposition;

import java.util.ArrayList;
import java.util.Random;

public abstract class Multiplication {
    public Random rand;

    /*
     * Precondition: the multipliers must each contain the same
     * number of notes (for use with voiceleading algorithms)
     */
    public int[][] multipliers;

    /*
     * For each note in multiplicand, select
     * a random multiplier, transpose it such that
     * its root is the note from multiplicand,
     * add the transposed version to the return value.
     * 
     * Be sure to clone the array from muliplier before
     * transposing it.
     */
    public abstract ArrayList<int[]> multiply(int[] multiplicand);

    /*
     * Using the helper method above, multiply all chord
     * in the input chord progression by randomly selected multipliers
     */
    public abstract ArrayList<int[]> multiply(ArrayList<int[]> multiplicands);

    /*
     * generate an intial progression,
     * multiply(multipier[rand.nextInt(multipier.length)])
     * and pass it through
     * the multiply methon above as many times as specified by
     * depth
     */
    public abstract ArrayList<int[]> generateProgression(int depth);
}
