// Driver for the authors' checker (hidny/CuboidSimplePhaseNetSearch, OutputReader.ValidNetSolutionChecker).
// Reads a net as "x,y;x,y;..." and asks hasSolution() for every box given on the command line (a,b,c).
import java.nio.file.*;
import OutputReader.ValidNetSolutionChecker;
public class CheckNet {
    public static void main(String[] args) throws Exception {
        String[] toks = new String(Files.readAllBytes(Paths.get(args[0]))).trim().split(";");
        int n = toks.length, minx = Integer.MAX_VALUE, miny = Integer.MAX_VALUE, maxx = Integer.MIN_VALUE, maxy = Integer.MIN_VALUE;
        int[][] c = new int[n][2];
        for (int k = 0; k < n; k++) { String[] p = toks[k].split(","); c[k][0] = Integer.parseInt(p[0].trim()); c[k][1] = Integer.parseInt(p[1].trim());
            minx = Math.min(minx, c[k][0]); maxx = Math.max(maxx, c[k][0]); miny = Math.min(miny, c[k][1]); maxy = Math.max(maxy, c[k][1]); }
        int H = Math.max(maxx - minx + 3, 2 * n), W = Math.max(maxy - miny + 3, 2 * n);   // pad by one cell on every side
        boolean[][] grid = new boolean[H][W];
        for (int k = 0; k < n; k++) grid[c[k][0] - minx + 1][c[k][1] - miny + 1] = true;
        System.out.println("net with " + n + " cells");
        for (int a = 1; a < args.length; a++) {
            String[] d = args[a].split(",");
            int[] dims = {Integer.parseInt(d[0]), Integer.parseInt(d[1]), Integer.parseInt(d[2])};
            long t0 = System.currentTimeMillis();
            boolean ok = ValidNetSolutionChecker.hasSolution(dims, grid);
            System.out.println(args[a].replace(',', 'x') + " : " + (ok ? "FOLDS" : "does not fold") + "  (" + (System.currentTimeMillis() - t0) + " ms)");
        }
    }
}
