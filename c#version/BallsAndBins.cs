public class BallsAndBins
{
    public static List<Bin> SortPerLowerBound(List<Bin> binList)
    {
        if (binList.Count <= 1) return binList;

        int mid = binList.Count / 2;
        var left = SortPerLowerBound(binList.Take(mid).ToList());
        var right = SortPerLowerBound(binList.Skip(mid).ToList());

        return Merge(left, right);
    }

    private static List<Bin> Merge(List<Bin> left, List<Bin> right)
    {
        var result = new List<Bin>();
        int i = 0, j = 0;

        while (i < left.Count && j < right.Count)
        {
            if (left[i].LowerLimit < right[j].LowerLimit)
            {
                result.Add(left[i]);
                i++;
            }
            else
            {
                result.Add(right[j]);
                j++;
            }
        }

        result.AddRange(left.Skip(i));
        result.AddRange(right.Skip(j));

        return result;
    }

    public static double CalculateSolValue(List<Bin> bins)
    {
        return bins.Sum(bin => bin.CurrentValue);
    }

    public static List<Solution> Border(Solution solution)
    {
        var neighbors = new List<Solution>();

        foreach (var iBin in solution.Bins)
        {
            if (!iBin.IsValidToTake()) continue;

            var targetSolution = new Solution(solution.Value, CloneBins(solution.Bins));
            var oldIBinValue = iBin.CurrentValue;

            foreach (var jBin in targetSolution.Bins)
            {
                if (jBin.Id == iBin.Id || !jBin.IsValidToPut()) continue;

                var newIBinValue = iBin.SetBalls(iBin.NumberOfBalls - 1);
                var diffIBinValue = Math.Abs(oldIBinValue - newIBinValue);

                var oldJBinValue = jBin.CurrentValue;
                var newJBinValue = jBin.SetBalls(jBin.NumberOfBalls + 1);
                var diffJBinValue = Math.Abs(newJBinValue - oldJBinValue);

                targetSolution.Value = solution.Value - diffIBinValue + diffJBinValue;
                neighbors.Add(new Solution(targetSolution.Value, CloneBins(targetSolution.Bins)));
            }
        }

        return neighbors;
    }

    private static List<Bin> CloneBins(List<Bin> bins)
    {
        return bins.Select(bin => new Bin(bin.Id, bin.LowerLimit, bin.UpperLimit) { NumberOfBalls = bin.NumberOfBalls }).ToList();
    }

    public static Solution BuscaLocal(Solution solution)
    {
        double bestValue = CalculateSolValue(solution.Bins);
        Solution bestSolution = solution;
        bool improved;

        do
        {
            improved = false;
            foreach (var neighbor in Border(solution))
            {
                double neighborValue = CalculateSolValue(neighbor.Bins);
                if (neighborValue > bestValue)
                {
                    bestValue = neighborValue;
                    bestSolution = neighbor;
                    improved = true;
                }
            }
        } while (improved);

        return bestSolution;
    }

    public static void Main(string[] args)
    {
        var lines = File.ReadAllLines("./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt");

        int numBins = int.Parse(lines[0]);
        int numBalls = int.Parse(lines[1]);

        var currentBinList = new List<Bin>();

        for (int i = 2; i < lines.Length; i++)
        {
            var parts = lines[i].Split(' ');
            int lowerLimit = int.Parse(parts[0]);
            int upperLimit = int.Parse(parts[1]);
            var bin = new Bin(i - 1, lowerLimit, upperLimit);
            bin.SetBalls(100);
            currentBinList.Add(bin);
        }

        var targetSolution = new Solution(CalculateSolValue(currentBinList), currentBinList);

        Console.WriteLine("Target Solution:");
        foreach (var bin in targetSolution.Bins)
        {
            Console.WriteLine($"Bin {bin.Id}: {bin.NumberOfBalls}");
        }

        Console.WriteLine("\nNeighbors:");
        var neighbors = Border(targetSolution);
        for (int i = 0; i < neighbors.Count; i++)
        {
            Console.WriteLine($"\nSolution {i}:");
            foreach (var bin in neighbors[i].Bins)
            {
                Console.WriteLine($"Bin {bin.Id}: {bin.NumberOfBalls}");
            }
        }
    }
}
