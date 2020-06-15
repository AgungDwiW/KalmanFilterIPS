package com.example.trilateration;

import java.util.Arrays;
//implementation 'org.apache.commons:commons-math3:3.6.1'
import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.MatrixUtils;


public class KalmanFilter {
    RealMatrix u;
    RealMatrix x; // Initial State
    RealMatrix A; // State Transition Matrix
    RealMatrix B; // Control Input Matrix
    RealMatrix H; // Measurement Mapping Matrix
    RealMatrix Q; // Process Noise Covariance
    RealMatrix R; // Measurement Noise Covariance
    RealMatrix P; // Covariance Matrix


    public KalmanFilter(double dt, double u_x, double u_y, double std_acc, double x_std_meas,
                        double y_std_meas, double init_x, double init_y) {
		/*
        :param dt: sampling time (time for 1 cycle)
        :param u_x: acceleration in x-direction
        :param u_y: acceleration in y-direction
        :param std_acc: process noise magnitude
        :param x_std_meas: standard deviation of the measurement in x-direction
        :param y_std_meas: standard deviation of the measurement in y-direction
        */
        //Define the  control input variables
        double[][] temp ={{u_x}, {u_y}};
        this.u = new  Array2DRowRealMatrix(temp);

        //Intial State
        double[][] temp2 ={{init_x}, {init_y}, {u_x}, {u_y}};
        this.x = new  Array2DRowRealMatrix(temp2);

        // Define the State Transition Matrix A
        double[][] temp3 = {{ 1, 0,dt, 0},
                { 0, 1, 0,dt},
                { 0, 0, 1, 0},
                { 0, 0, 0, 1}};
        this.A = new  Array2DRowRealMatrix(temp3);

        //# Define the Control Input Matrix B
        double[][] temp4 = {{ Math.pow(dt,2)/2, 0},
                { Math.pow(dt,2)/2, 0},
                {               dt, 0},
                {                0,dt}};
        this.B = new  Array2DRowRealMatrix(temp4);

        //# Define Measurement Mapping Matrix

        double [][] temp5 = {{1, 0, 0, 0},
                {0, 1, 0, 0}};
        this.H = new  Array2DRowRealMatrix(temp5);

        //Initial Process Noise Covariance
        double std = Math.pow(std_acc, 2);
        double dt4 = Math.pow(dt,4)/4 *std;
        double dt3 = Math.pow(dt,3)/2 * std;
        double dt2 = Math.pow(dt,2) *std;

        double [][] temp6 = {{ dt4,   0, dt3,   0},
                {   0, dt4,   0, dt3},
                { dt3,   0, dt2,   0},
                {   0, dt3,   0, dt2}
        };
        this.Q = new  Array2DRowRealMatrix(temp6);

        //#Initial Measurement Noise Covariance
        double [][] temp7 = {{Math.pow(x_std_meas,2),                      0},
                {                     0, Math.pow(y_std_meas,2)}};
        this.R = new  Array2DRowRealMatrix(temp7);

        //Initial Covariance Matrix

        this.P = new  Array2DRowRealMatrix( eye(A.getRow(0).length));
    }


    public double [][] eye(int shape){
        double [][] ret = new double [shape][shape];
        for (int x = 0; x<shape; x++) {
            for (int y = 0; y<shape; y++) {
                if (x == y)
                    ret [x][y] = 1;
                else
                    ret [x][y] = 0;
            }
        }
        return ret;
    }

    public double[][] predict(){
        // Update time state
        // x_k =Ax_(k-1) + Bu_(k-1)
        this.x = this.A.multiply(this.x).add(this.B.multiply(this.u));

        // Calculate error covariance
        // P= A*P*A' + Q
        this.P = this.A.multiply(this.P).multiply(this.A.transpose()).add(this.Q);
        return Arrays.copyOfRange(this.x.getData(), 0, 2);
    }

    public double[][] update(double [][] z){
        // S = H*P*H'+R
        RealMatrix S = this.H.multiply(this.P.multiply(this.H.transpose())).add(this.R);

        // Calculate the Kalman Gain
        // K = P * H'* inv(H*P*H'+R)
        RealMatrix K = this.P.multiply(this.H.transpose()).multiply(MatrixUtils.inverse(S));
        RealMatrix zx = new  Array2DRowRealMatrix(z);
        this.x = x.add(K.multiply(zx.subtract(H.multiply(x))));

        // Update error covariance matrix
        RealMatrix I = new  Array2DRowRealMatrix(eye(this.H.getRow(0).length));
        this.P = I.subtract(K.multiply(this.H)).multiply(this.P);

        return Arrays.copyOfRange(this.x.getData(), 0, 2);
    }
}
