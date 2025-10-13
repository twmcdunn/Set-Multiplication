package org.delightofcomposition.voiceleading;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public class VoiceLeading extends VoiceLeadingFramework implements Directed, NoCommons, NoCommonsDirected {

    public ArrayList<ArrayList<Integer>> getAllOrders(ArrayList<Integer> notesToOrder) {
        ArrayList<ArrayList<Integer>> orders = new ArrayList<ArrayList<Integer>>();

        if (notesToOrder.size() > 1) {
            for (int i = 0; i < notesToOrder.size(); i++) {
                ArrayList<Integer> remaining = new ArrayList<Integer>(notesToOrder);
                remaining.remove(i);
                int firstNote = notesToOrder.get(i);

                ArrayList<ArrayList<Integer>> ordersOfRemaining = getAllOrders(remaining);
                for (ArrayList<Integer> order : ordersOfRemaining) {
                    ArrayList<Integer> completeOrder = new ArrayList<Integer>();
                    completeOrder.add(firstNote);
                    completeOrder.addAll(order);
                    orders.add(completeOrder);
                }
            }
        } else {
            ArrayList<Integer> singleOrder = new ArrayList<Integer>(notesToOrder);
            orders.add(singleOrder);
        }
        return orders;
    }

    // @Precondition: firstChord and secondChord have the same number of notes
    public int[] optimalVoiceLeading(int[] firstChord, int[] secondChord, Heuristic heuristic) {
        int tet = 12;
        ArrayList<Integer> secondChordAsArrayList = arrToArrList(secondChord);
        ArrayList<ArrayList<Integer>> allOrders = getAllOrders(secondChordAsArrayList);

        int[] bestOrder = null;// dummy values
        int smallestHeuresticValue = Integer.MAX_VALUE;
        for (ArrayList<Integer> order : allOrders) {
            int[] orderInBestOctaves = new int[secondChord.length];
            for (int i = 0; i < firstChord.length; i++) {
                orderInBestOctaves[i] = pitchInClosestOct(firstChord[i], order.get(i));
            }
            int heuresticValue = heuristic.getValue(firstChord, orderInBestOctaves);
            if (heuresticValue < smallestHeuresticValue) {
                smallestHeuresticValue = heuresticValue;
                bestOrder = orderInBestOctaves;
            }
        }
        return bestOrder;
    }

    public int[] stepwiseVoiceLeading(int[] firstChord, int[] secondChord) {
        return optimalVoiceLeading(firstChord, secondChord, (f, s) -> {
            int tot = 0;
            for (int i = 0; i < f.length; i++) {
                tot += Math.abs(f[i] - s[i]);
            }
            return tot;
        });
    };

    public int[] directedVoiceLeading(int[] firstChord, int[] secondChord, int target) {
        return optimalVoiceLeading(firstChord, secondChord, (f, s) -> {
            int furthest = 0;
            for (int i = 0; i < f.length; i++) {
                furthest = Math.max(Math.abs(s[i] - target), furthest);
            }
            return furthest;
        });
    }

    public int[] uncommonVoiceLeading(int[] firstChord, int[] secondChord) {
        return optimalVoiceLeading(firstChord, secondChord, (f, s) -> {
            int tot = 0;
            for (int i = 0; i < f.length; i++) {
                if (f[i] == s[i])
                    return Integer.MAX_VALUE;
                tot += Math.abs(f[i] - s[i]);
            }
            return tot;
        });
    }

    public int[] uncommonDirectedVoiceLeading(int[] firstChord, int[] secondChord, int target) {
        return optimalVoiceLeading(firstChord, secondChord, (f, s) -> {
            int furthest = 0;
            for (int i = 0; i < f.length; i++) {
                if (f[i] == s[i])
                    return Integer.MAX_VALUE;
                furthest = Math.max(Math.abs(s[i] - target), furthest);
            }
            return furthest;
        });
    }

    public ArrayList<Integer> arrToArrList(int[] arr) {
        return new ArrayList<Integer>(Arrays.stream(arr).boxed().collect(Collectors.toList()));
    }

    public int pitchInClosestOct(int target, int pc) {
        int tet = 12;
        int oct = (int) Math.rint((target - pc) / (double) tet);
        return oct * tet + pc;
    }
}
