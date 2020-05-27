package com.example.trilateration;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Layout;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import com.opencsv.CSVWriter;

import static android.os.SystemClock.sleep;
import static java.lang.Math.pow;

public class MainActivity extends AppCompatActivity {
    //customable var
    public int sampling_rate = 25; // how many sample taken to get a coordinate
    public int sleep_time = 40; // how much time interval between each sample

    /* Kalman Filter args
    :param dt: sampling time (time for 1 cycle)
    :param u_x: acceleration in x-direction
    :param u_y: acceleration in y-direction
    :param std_acc: process noise magnitude
    :param x_std_meas: standard deviation of the measurement in x-direction
    :param y_std_meas: standard deviation of the measurement in y-direction
    */
    private KalmanFilter KF = new KalmanFilter(0.1, 1, 1, 1, 0.1,0.1);

    /* Current setting
     * SSID	                BSSID       	    A	        N
     * Ephemeral blessing	ce:73:14:c4:7a:28	-63.555	    2.18345215481207
     * Elfais	            18:0f:76:91:f2:72	-47.43	    3.40041922816446
     * TP-LINK_E630	        c0:25:e9:7a:e6:30	-54.685	    2.87070468917083
     *
     * A = RSSI taken at 1 meter point
     * N = noise covariance calculated from experiment
     */

    public String BSSID1 = "ce:73:14:c4:7a:28";
    public double A1 = -63.555;
    public double N1 = 2.18345215481207;
    public int x1 = 320;
    public int y1 = 0;

    public String BSSID2 = "18:0f:76:91:f2:72";
    public double A2 = -47.43;
    public double N2 = 3.40041922816446;
    public int x2 = 0;
    public int y2 = 460;

    public String BSSID3 = "c0:25:e9:7a:e6:2f";
    public double A3 = -54.685;
    public double N3 = 2.87070468917083;
    public int x3 = 475;
    public int y3 = 460;

    //console
    public TextView console;
    public int n;
    public List<String[]> log = new ArrayList<String[]>(); //to save the measurements to csv
    private String csv;

    //wifi scaner
    private WifiManager wifiManager;
    private int size = 0;


    public int flag = 1;
    //cordinates
    public TextView measured, predicted, estimated;
    public Button start;
    public TextView dist1,dist2,dist3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /* ==================
          setting variables
        ======================*/
        //coord
        measured = findViewById(R.id.measured);
        predicted = findViewById(R.id.predicted);
        estimated = findViewById(R.id.estimated);
        dist1 = findViewById(R.id.dist1);
        dist2 = findViewById(R.id.dist2);
        dist3 = findViewById(R.id.dist3);

        //console
        console = findViewById(R.id.console);
        console.setMovementMethod(new ScrollingMovementMethod());
        n=1;
        TextView print = findViewById(R.id.print);
        TextView clear = findViewById(R.id.clear);
        print.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                printCSV();

            }
        });
        print.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                log.clear();

            }
        });

        // wifi manager
        wifiManager = (WifiManager)
                getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        /* ==================
          Creating log header
        ======================*/
        ArrayList<String> temp = new ArrayList<>();
        temp.add("rssi1" );
        temp.add("distance1");
        temp.add("rssi2" );
        temp.add("distance2");
        temp.add("rssi3" );
        temp.add("distance3");
        temp.add("x measured" );
        temp.add("y measured");
        temp.add("x predicted" );
        temp.add("y predicted");
        temp.add("x estimated" );
        temp.add("y estimated");
        String [] temp2 = new String[temp.size()];
        temp2 = temp.toArray(temp2);
        log.add(temp2);

        /* ==================
          Starting background scanning
        ======================*/
        start = findViewById(R.id.start);
        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                flag *=-1; new ScanWifi().execute();

            }
        });

    }

    public double getDistance(double RSSI, double A,  double N ){
        return pow(10, -1*((RSSI-A)/(10*N)));
    }


    private class ScanWifi extends AsyncTask<String, Void, String> {
        // daemon class to get rssi and freq of certain wifi
        double level1,level2,level3;
        int counter1  ,counter2 ,counter3;

        @Override
        protected String doInBackground(String... params) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    printConsole("scanning data;");
                    printConsole("--------------------- ");
                }
            });
            while(true) {
                //main loop
                if (flag == 1) { //stop
                    return "ended";
                }
                List<ScanResult> results;

                level1 = level2 = level3 = 0;
                counter1 = counter2 = counter3=0;

                for (int x = 0; x < sampling_rate; x++) {
                    //======================================================================
                    //getting rssi
                    //======================================================================

                    if (!wifiManager.startScan()) {
                        x -= 1;
                        continue;
                    }
                    results = wifiManager.getScanResults();
                    for (ScanResult scanResult : results) {
                        //assigning the rssis
                        if (scanResult.BSSID.equals(BSSID1)) {
                            level1 += scanResult.level;
                            counter1 += 1;
                        } else if (scanResult.BSSID.equals(BSSID2)) {
                            level2 += scanResult.level;
                            counter2 += 1;
                        } else if (scanResult.BSSID.equals(BSSID3)) {
                            level3 += scanResult.level;
                            counter3 += 1;
                        }
                    }
                    /*
                    final int xx = x;

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole(xx + "/" + sampling_rate);
                        }
                    });
                    */
                    sleep(sleep_time);
                }

                //======================================================================
                //process the rssi
                //======================================================================
                double dist1,dist2,dist3;
                final double distance1, distance2, distance3;

                dist1 = dist2 = dist3 = 0;
                if(counter1 != 0) {
                    level1 = level1 / counter1;
                    dist1 = getDistance(level1, A1, N1) *100;
                }
                if(counter2 != 0) {
                    level2 = level2 / counter2;
                    dist2 = getDistance(level2, A2, N2) * 100;
                }
                if(counter3 != 0) {
                    level3 = level3 / counter3;
                    dist3 = getDistance(level3, A3, N3) * 100;
                }

                distance1 = dist1; distance2 = dist2; distance3 = dist3;

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        changeDist(Math.round(distance1*100)/100+"", Math.round(distance2*100)/100+"", Math.round(distance3*100)/100+"");
                    }
                });

                if (!(counter1 == 0 || counter2 == 0 || counter3 == 0)){
                    //======================================================================
                    //calculate the coordinate
                    //======================================================================
                    final double[][] coord = getCoord(distance1,distance2, distance3);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole("===================================");
                            printConsole("rssi1 : " + level1);
                            printConsole("rssi2 : " + level2);
                            printConsole("rssi3: " + level3);
                            printConsole("distance 1 :" + distance1);
                            printConsole("distance 2 :" + distance2);
                            printConsole("distance 3 :" + distance3);

                        }
                    });

                    //======================================================================
                    //apply kalman filter
                    //======================================================================
                    final double [][] predi = KF.predict();
                    final double[][] update = KF.update(coord);

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole("-----------------------------------");
                            printConsole("measured : " + coord[0][0] + ","+coord[1][0] );
                            printConsole("predicted : " + predi[0][0] + ","+predi[1][0]);
                            printConsole("estimated : " + update[0][0] + ","+update[1][0]);
                            printConsole("===================================");
                            changeCoor(coord, predi, update);
                        }
                    });

                    //======================================================================
                    //saving log
                    //======================================================================
                    ArrayList<String> temp = new ArrayList<>();
                    temp.add("" + level1);
                    temp.add(""+ distance1);
                    temp.add("" + level2);
                    temp.add(""+ distance2);
                    temp.add("" + level3);
                    temp.add(""+ distance3);
                    temp.add(""+ coord[0][0]);
                    temp.add(""+ coord[1][0]);
                    temp.add(""+ predi[0][0]);
                    temp.add(""+ predi[1][0]);
                    temp.add(""+ update[0][0]);
                    temp.add(""+ update[1][0]);
                    String [] temp2 = new String[temp.size()];
                    temp2 = temp.toArray(temp2);
                    log.add(temp2);


                }
                else{
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole("===================================");
                            printConsole("rssi missing");
                            printConsole("===================================");
                            double [][] dummy ={{-1},{-1}};
                            changeCoor(dummy, dummy, dummy);
                        }
                    });
                }
            }
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);

            flag *=-1;

        }
    }

    public void changeCoor(double [][] meas, double[][] pred, double[][] estim){
        //utility function to change text
        DecimalFormat df = new DecimalFormat("#.0");
        measured.setText("" + df.format(meas[0][0]) + "," + df.format(meas[1][0]));
        predicted.setText("" + df.format(pred[0][0]) + "," + df.format(pred[1][0]));
        estimated.setText("" + df.format(estim[0][0]) + "," + df.format(estim[1][0]));
    }

    public void changeDist(String d1, String d2, String d3){
        //utility function to change text
        dist1.setText(d1);
        dist2.setText(d2);
        dist3.setText(d3);
    }

    private void printCSV(){
        //utility function to print csv
        try {
            String uuid = UUID.randomUUID().toString();
            csv = (getExternalFilesDir(null) + "/log"+uuid + ".csv"); // Here csv file name is MyCsvFile.csv
            CSVWriter writer = null;
            writer = new CSVWriter(new FileWriter(csv));
            writer.writeAll(log);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        printConsole("exported all "+ log.size() + "data to "+ csv);
    }



    public void printConsole(String s){
        // Function to print to console
        if(n%1000 == 0 && n != 0){

            console.setText(n+": "+ s +"\n");
            n+=1;
            return;
        }

        console.append(n+": "+ s +"\n");
        n+=1;
        final Layout layout = console.getLayout();
        if(layout != null){
            int scrollDelta = layout.getLineBottom(console.getLineCount() - 1)
                    - console.getScrollY() - console.getHeight();
            if(scrollDelta > -1)
                console.scrollBy(0, scrollDelta);
        }
    }


    public double[][] getCoord(double r1, double r2, double  r3){
        //calculate trilateration from 3 radius return {{x},{y}}

        double A, B, C, D, E, F, x,y;
        double [][]  result = {{-1},{-1}};
        A = 2*x2 - 2*x1;
        B = 2*y2 - 2*y1;
        C = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2;
        D = 2*x3 - 2*x2;
        E = 2*y3 - 2*y2;
        F = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3;
        x = (C*E - F*B) / (E*A - B*D);
        y = (C*D - A*F) / (B*D - A*E);
        result[0][0] = x;
        result[1][0] = y;
        return result;
    }




}
