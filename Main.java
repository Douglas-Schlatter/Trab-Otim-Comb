import java.io.*;
import java.util.*;


public class Main {

    public static void main(String[] args) throws IOException {
        // Abrir o arquivo
        File file = new File("./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt");
        BufferedReader br = new BufferedReader(new FileReader(file));

        // Ler linhas do arquivo
        List<String> lines = new ArrayList<>();
        String line;
        while ((line = br.readLine()) != null) {
            lines.add(line);
        }
        br.close();

        // Lista de bins contendo índice, limite inferior e limite superior
        List<Bin> currentBinList = new ArrayList<>();

        int numBins = Integer.parseInt(lines.get(0));
        int numBalls = Integer.parseInt(lines.get(1));

        for (int index = 2; index < lines.size(); index++) {
            String[] targetLine = lines.get(index).split(" ");
            int lowerLimit = Integer.parseInt(targetLine[0]);
            int upperLimit = Integer.parseInt(targetLine[1]);

            Bin targetBin = new Bin(index - 1, lowerLimit, upperLimit);
            targetBin.setBalls(100);
            currentBinList.add(targetBin);
        }

        Solution targetSolution = new Solution(calculateSolValue(currentBinList), currentBinList);

        // Exibir solução alvo
        System.out.println("TargetSolution");
        for (Bin bin : targetSolution.getBins()) {
            System.out.print(bin.getId() + " " + bin.getNumberOfBalls() + "| ");
        }

        System.out.println("\nVizinhos");
        List<Solution> neighbors = border(targetSolution);
        for (int i = 0; i < neighbors.size(); i++) {
            System.out.println("\nSol " + i);
            for (Bin bin : neighbors.get(i).getBins()) {
                System.out.print(bin.getId() + " " + bin.getNumberOfBalls() + "| ");
            }
        }
    }

    public static List<Bin> sortPerLowerBound(List<Bin> binList) {
        if (binList.size() > 1) {
            int mid = binList.size() / 2;

            List<Bin> left = new ArrayList<>(binList.subList(0, mid));
            List<Bin> right = new ArrayList<>(binList.subList(mid, binList.size()));

            sortPerLowerBound(left);
            sortPerLowerBound(right);

            int i = 0, j = 0, k = 0;

            while (i < left.size() && j < right.size()) {
                if (left.get(i).getLowerLimit() < right.get(j).getLowerLimit()) {
                    binList.set(k++, left.get(i++));
                } else {
                    binList.set(k++, right.get(j++));
                }
            }

            while (i < left.size()) {
                binList.set(k++, left.get(i++));
            }

            while (j < right.size()) {
                binList.set(k++, right.get(j++));
            }
        }
        return binList;
    }

    public static double calculateSolValue(List<Bin> solution) {
        return solution.stream().mapToDouble(Bin::getCurrentValue).sum();
    }

    public static List<Solution> border(Solution solution) {
        List<Solution> neighbors = new ArrayList<>();
        for (Bin iBin : solution.getBins()) {
            if (iBin.isValidToTake()) {
                double oldIBinValue = iBin.getCurrentValue();
                for (Bin jBin : solution.getBins()) {
                    if (jBin.getId() != iBin.getId() && jBin.isValidToPut()) {
                        int newIBinBalls = iBin.getNumberOfBalls() - 1;
                        double newIBinValue = iBin.setBalls(newIBinBalls);

                        double diffIBinValue = Math.abs(oldIBinValue - newIBinValue);

                        double oldJBinValue = jBin.getCurrentValue();
                        int newJBinBalls = jBin.getNumberOfBalls() + 1;
                        double newJBinValue = jBin.setBalls(newJBinBalls);

                        double diffJBinValue = Math.abs(newJBinValue - oldJBinValue);

                        double newValue = solution.getValue() - diffIBinValue + diffJBinValue;

                        Solution newSolution = new Solution(newValue, cloneBins(solution.getBins()));
                        neighbors.add(newSolution);
                    }
                }
            }
        }
        return neighbors;
    }

    public static List<Bin> cloneBins(List<Bin> bins) {
        List<Bin> clonedBins = new ArrayList<>();
        for (Bin bin : bins) {
            clonedBins.add(new Bin(bin.getId(), bin.getLowerLimit(), bin.getUpperLimit(), bin.getNumberOfBalls()));
        }
        return clonedBins;
    }

    public static Solution buscaLocal(Solution solucao) {
        double bestValue = calculateSolValue(solucao.getBins());
        Solution bestSol = solucao;
        boolean improved = true;

        while (improved) {
            improved = false;
            for (Solution neighbor : border(solucao)) {
                double neighborValue = calculateSolValue(neighbor.getBins());
                if (neighborValue > bestValue) {
                    bestValue = neighborValue;
                    bestSol = neighbor;
                    improved = true;
                }
            }
        }
        return bestSol;
    }
}
