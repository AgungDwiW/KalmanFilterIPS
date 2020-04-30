package com.example.trilateration;

import androidx.appcompat.app.AppCompatActivity;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Layout;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import static android.os.SystemClock.sleep;
import static java.lang.Math.pow;

public class MainActivity extends AppCompatActivity {
    //console
    public TextView console;
    public int n;

    //wifi scaner
    private WifiManager wifiManager;
    private int size = 0;
    private List<ScanResult> results;

    public int flag = 1;
    //cordinates
    public TextView coord;
    public int x1, x2,x3,y1,y2,y3;
    public Button start;
    public String BSSID1,BSSID2, BSSID3;

    public TextView dist1,dist2,dist3;

    public double A1, A2, A3;
    public double N1, N2, N3;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /* ==================
          setting variables
        ======================*/
        //coord
        coord = findViewById(R.id.coord);
        dist1 = findViewById(R.id.dist1);
        dist2 = findViewById(R.id.dist2);
        dist3 = findViewById(R.id.dist3);
        //console
        console = findViewById(R.id.console);
        console.setMovementMethod(new ScrollingMovementMethod());
        n=1;
        /*
        SSID	            BSSID       	    A	        N
        Ephemeral blessing	ce:73:14:c4:7a:28	-63.555	    2.18345215481207
        Elfais	            18:0f:76:91:f2:72	-47.43	    3.40041922816446
        TP-LINK_E630	    c0:25:e9:7a:e6:30	-54.685	    2.87070468917083
         */
        BSSID1 = "ce:73:14:c4:7a:28";
        A1 = -63.555;
        N1 = 2.18345215481207;
        x1 = 320;
        y1 = 0;

        BSSID2 = "18:0f:76:91:f2:72";
        A2 = -47.43;
        N2 = 3.40041922816446;
        x2 = 0;
        y2 = 460;


        BSSID3 = "c0:25:e9:7a:e6:2f";
        A3 = -54.685;
        N3 = 2.87070468917083;
        x3 = 475;
        y3 = 460;


        // wifi manager
        wifiManager = (WifiManager)
                getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        /* ==================
          Starting background scanning
        ======================*/
        start = findViewById(R.id.start);
        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                flag *=-1; new scanWifi().execute();

            }
        });
    }

    public void changeDist(String d1, String d2, String d3){
        dist1.setText(d1);
        dist2.setText(d2);
        dist3.setText(d3);
    }

    public void printConsole(String s){
        // Function to print to console
        console.append(n+": "+ s +"\n");
        n+=1;
        final Layout layout = console.getLayout();
        if(layout != null){
            int scrollDelta = layout.getLineBottom(console.getLineCount() - 1)
                    - console.getScrollY() - console.getHeight();
            if(scrollDelta > 0)
                console.scrollBy(0, scrollDelta);
        }
    }

    public void changeCoord(String s){
        coord.setText(s);
    }

    public double[] getCoord(double r1, double r2, double  r3){
        double A, B, C, D, E, F, x,y;
        double []  result = {-1,-1};
        A = 2*x2 - 2*x1;
        B = 2*y2 - 2*y1;
        C = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2;
        D = 2*x3 - 2*x2;
        E = 2*y3 - 2*y2;
        F = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3;
        x = (C*E - F*B) / (E*A - B*D);
        y = (C*D - A*F) / (B*D - A*E);
        result[0] = x;
        result[1] = y;
        return result;
    }

    public double getDistance(double RSSI, double A,  double N ){
        return pow(10, -1*((RSSI-A)/(10*N)));
    }

    private class scanWifi extends AsyncTask<String, Void, String> {
        // daemon class to get rssi and freq of certain wifi
        double level1,level2,level3;
        int counter1 =0 ,counter2 =0 ,counter3=0;

        @Override
        protected String doInBackground(String... params) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    printConsole("scanning data;");
                    printConsole("--------------------- ");
                }
            });
            //main loop
            level1 = level2 = level3 = 0;
            for (int x=0; x<100; x++){
                if (flag == 1){
                    break;}

                results = wifiManager.getScanResults();
                for (ScanResult scanResult : results) {
                    //assigning the rssis
                    if(scanResult.BSSID.equals(BSSID1) ){
                        level1 += scanResult.level; counter1+=1;}
                    else if (scanResult.BSSID.equals(BSSID2)){
                        level2 += scanResult.level; counter2+=1;}
                    else if (scanResult.BSSID.equals(BSSID3)){
                        level3 += scanResult.level; counter3+=1;}
                }
                sleep(10);
                if (x%10 ==0){
                    final int xx = x;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole(xx+"/300");
                        }
                    });
                }


            }
            return "aaaa";
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
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
                double[] coord = getCoord(distance1,distance2, distance3);
                final String coordString = "" +Math.round(coord[0]*100)/100 + "," + Math.round(coord[1]*100)/100;
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
                        printConsole("coordinate : " + coordString);
                        printConsole("===================================");
                        changeCoord(coordString);
                    }
                });
            }

            else{
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        printConsole("===================================");
                        printConsole("rssi missing");
                        printConsole("===================================");
                        changeCoord("x,x");
                    }
                });
            }

        }
    }

}
