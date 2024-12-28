import java.util.List;

public class Solution {
    private double value;
    private List<Bin> bins; // Presumindo que "bins" seja uma lista de objetos da classe Bin
    private double targetSolValue;

    public Solution(double value, List<Bin> bins) {
        this.value = value;
        this.bins = bins;
    }

    public void setSolValue(double targetSolValue) {
        this.targetSolValue = targetSolValue;
    }

    // Getters e Setters (opcional, dependendo da necessidade)
    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public List<Bin> getBins() {
        return bins;
    }

    public void setBins(List<Bin> bins) {
        this.bins = bins;
    }

    public double getTargetSolValue() {
        return targetSolValue;
    }
}
