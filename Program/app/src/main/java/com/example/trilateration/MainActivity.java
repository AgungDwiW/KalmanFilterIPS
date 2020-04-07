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

public class MainActivity extends AppCompatActivity {
    //console
    public TextView console;
    public int n;

    //wifi scaner
    private WifiManager wifiManager;
    private ListView listView;
    private int size = 0;
    private List<ScanResult> results;
    public List<String[]> results_all = new ArrayList<String[]>();
    public ArrayList<String> arrayList = new ArrayList<>();
    private ArrayAdapter adapter;
    public int flag = -1;
    public scanWifi scan;
    //cordinates
    public TextView coord;
    public TextView t_wifi1, t_wifi2, t_wifi3, t_x1, t_x2, t_x3, t_y1, t_y2, t_y3;
    public int x1, x2,x3,y1,y2,y3;
    public Button start;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /* ==================
          setting variables
        ======================*/
        //console
        console = findViewById(R.id.console);
        console.setMovementMethod(new ScrollingMovementMethod());
        n=1;

        //wifi credentials
//        t_wifi1 = findViewById(R.id.wifi1);
//        t_wifi2 = findViewById(R.id.wifi2);
//        t_wifi3 = findViewById(R.id.wifi3);
//        t_x1 = findViewById(R.id.x1);
//        t_x2 = findViewById(R.id.x2);
//        t_x3 = findViewById(R.id.x3);
//        t_y1 = findViewById(R.id.y1);
//        t_y2 = findViewById(R.id.y2);
//        t_y3 = findViewById(R.id.y3);
        x1 = 0;
        y1 = 0;
        x2 = 50;
        y2 = 100;
        x3 = 100;
        y3 = 0;

        //list view
        listView = findViewById(R.id.wifiList);
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, arrayList);
        listView.setAdapter(adapter);


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

    public double[] getDistance(double r1, double r2, double  r3){
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

    private class scanWifi extends AsyncTask<String, Void, String> {
        // daemon class to get rssi and freq of certain wifi


        @Override
        protected String doInBackground(String... params) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    printConsole("started;");
                    printConsole("--------------------- ");
                }
            });
            //main loop
            int level1,level2,level3;
            int freq1, freq2, freq3;
            while(true){
                if (flag == 1){
                    break;}
                arrayList.clear();
                level1 = level2 = level3 = -1;
                freq1 = freq2 = freq3 = -1;
                results = wifiManager.getScanResults();
                for (ScanResult scanResult : results) {
                    //assigning the rssis
                    if(scanResult.BSSID.equals("82:2a:69:53:0e:9a") ){

                        level1 = scanResult.level; freq1 = scanResult.frequency;}
                    else if (scanResult.BSSID.equals("c0:25:e9:7a:e6:30")){

                        level2 = scanResult.level;freq2 = scanResult.frequency;}
                    else if (scanResult.BSSID.equals("ce:73:14:c4:7a:28")){

                        level3 = scanResult.level;freq3 = scanResult.frequency;}
                    arrayList.add(scanResult.SSID + " - " + scanResult.BSSID + " - " + scanResult.level);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            adapter.notifyDataSetChanged();
                        }
                    });
                }
                //getting the distances
                final double distance1, distance2, distance3;
                if (!(level1 == -1 || level2 == -1 || level3 == -1)){
                    distance1 = Math.pow(10, ((double) freq1 - level1) / (10 * 2));
                    distance2 = Math.pow(10, ((double) freq2 - level2) / (10 * 2));
                    distance3 = Math.pow(10, ((double) freq3 - level3) / (10 * 2));
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            printConsole("===================================");
                            printConsole("distance 1 :" + distance1);
                            printConsole("distance 2 :" + distance2);
                            printConsole("distance 3 :" + distance3);
                            printConsole("===================================");

                        }
                    });
                    //======================================================================
                    //calculate the coordinate
                    //======================================================================


                }

                sleep(1000);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        printConsole("--------------------- ");
                    }
                });
            }
            return "aaaa";
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    printConsole("scanning done; Current data: " + results_all.size());
                }
            });
            // do something with result
        }
    }
    BroadcastReceiver wifiReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            results = wifiManager.getScanResults();
            unregisterReceiver(this);
            //ArrayList<String> temp = new ArrayList<>();
            //temp.add(coordinate.getText() +"");
            for (ScanResult scanResult : results) {
                //temp.add(scanResult.BSSID );
                //temp.add(scanResult.level+"");
                arrayList.add(scanResult.BSSID + " - " + scanResult.level);
                adapter.notifyDataSetChanged();
            }
            //String[] temp2 = new String[temp.size()];
            //temp2 = temp.toArray(temp2);
            //results_all.add(temp2);
        };
    };
}
