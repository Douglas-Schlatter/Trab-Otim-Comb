public class Bin {
    private int id;
    private int lowerLimit;
    private int upperLimit;
    private int numberOfBalls;
    private double currentValue;

    public Bin(int id, int lowerLimit, int upperLimit,int numberOfBalls) {
        this.id = id;
        this.lowerLimit = lowerLimit;
        this.upperLimit = upperLimit;
        this.numberOfBalls = numberOfBalls;
        this.currentValue = 0;
    }
    
    public Bin(int id, int lowerLimit, int upperLimit) {
        this.id = id;
        this.lowerLimit = lowerLimit;
        this.upperLimit = upperLimit;
        this.numberOfBalls = 0;
        this.currentValue = 0;
    }


    public double updateValue() {
        this.currentValue = this.numberOfBalls * (this.numberOfBalls + 1) / 2.0;
        return this.currentValue;
    }

    public double setBalls(int targetNumBalls) {
        this.numberOfBalls = targetNumBalls;
        return updateValue();
    }

    public boolean isValidToPut() {
        return this.numberOfBalls + 1 <= this.upperLimit;
    }

    public boolean isValidToTake() {
        return this.numberOfBalls - 1 >= this.lowerLimit;
    }

    // Getters and Setters (opcional, dependendo da necessidade)
    public int getId() {
        return id;
    }

    public int getLowerLimit() {
        return lowerLimit;
    }

    public int getUpperLimit() {
        return upperLimit;
    }

    public int getNumberOfBalls() {
        return numberOfBalls;
    }

    public double getCurrentValue() {
        return currentValue;
    }
}
