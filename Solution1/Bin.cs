public class Bin
{
    public int id 
    public int lowerLimit
    public int upperLimit 
    public int numberOfBalls 
    public double currentValue 

    public Bin(int id, int lowerLimit, int upperLimit)
    {
        this.id = id;
        this.lowerLimit = lowerLimit;
        this.upperLimit = upperLimit;
        numberOfBalls = 0;
        currentValue = 0;
    }

    public double UpdateValue()
    {
        currentValue = numberOfBalls * (numberOfBalls + 1) / 2.0;
        return currentValue;
    }

    public double SetBalls(int targetNumBalls)
    {
        numberOfBalls = targetNumBalls;
        return UpdateValue();
    }

    public bool IsValidToPut()
    {
        return numberOfBalls + 1 <= upperLimit;
    }

    public bool IsValidToTake()
    {
        return numberOfBalls - 1 >= lowerLimit;
    }
}
