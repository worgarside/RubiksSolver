public class Solver {
    enum Direction{TOP, BOTTOM, LEFT, RIGHT, FRONT, BACK};

    public static void main(String[] args) {
        Cube rubiksCube = newCube();
        System.out.println(rubiksCube);
        System.out.println("-------------------------------------------------------- \n");

        rubiksCube.moveR();
        System.out.println(rubiksCube);
        System.out.println("-------------------------------------------------------- \n");

        rubiksCube.moveU();
        System.out.println(rubiksCube);
        System.out.println("-------------------------------------------------------- \n");

        rubiksCube.moveNotL();
        System.out.println(rubiksCube);
        System.out.println("-------------------------------------------------------- \n");
    }

    public static Cube newCube() {
        Side top = new Side('W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W');
        Side bottom = new Side('Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y');
        Side left = new Side('O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O');
        Side right = new Side('R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R');
        Side front = new Side('G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G');
        Side back = new Side('B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B');

        Cube tempCube = new Cube(top, bottom, left, right, front, back);

        return tempCube;
    }
}