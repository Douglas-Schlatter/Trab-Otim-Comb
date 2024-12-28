public class Solution
{
    public double value 
    public List<Bin> bins 
    public double targetSolValue 

    public Solution(double value, List<Bin> bins)
    {
        this.value = value;
        this.bins = bins;
    }

    public void SetSolValue(double targetSolValue)
    {
        this.targetSolValue = targetSolValue;
    }
}