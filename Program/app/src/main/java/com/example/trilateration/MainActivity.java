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
import android.widget.ArrayAdapter;
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

    //cordinates
    public TextView coord;
    public TextView t_wifi1, t_wifi2, t_wifi3, t_x1, t_x2, t_x3, t_y1, t_y2, t_y3;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /* ==================
          setting variables
        ======================*/
        //console
        console = findViewById(R.id.console);
        n=1;

        //wifi credentials
        t_wifi1 = findViewById(R.id.wifi1);
        t_wifi2 = findViewById(R.id.wifi2);
        t_wifi3 = findViewById(R.id.wifi3);
        t_x1 = findViewById(R.id.x1);
        t_x2 = findViewById(R.id.x2);
        t_x3 = findViewById(R.id.x3);
        t_y1 = findViewById(R.id.y1);
        t_y2 = findViewById(R.id.y2);
        t_y3 = findViewById(R.id.y3);

        /* ==================
          Starting background scanning
        ======================*/
        new scanWifi().execute();
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
                level1 = level2 = level3 = -1;
                freq1 = freq2 = freq3 = -1;
                for (ScanResult scanResult : results) {
                    //assigning the rssis
                    if(scanResult.BSSID == t_wifi1.getText()){
                        level1 = scanResult.level; freq1 = scanResult.frequency;}
                    else if (scanResult.BSSID == t_wifi2.getText()){
                        level2 = scanResult.level;freq2 = scanResult.frequency;}
                    else if (scanResult.BSSID == t_wifi3.getText()){
                        level3 = scanResult.level;freq3 = scanResult.frequency;}
                    arrayList.add(scanResult.BSSID + " - " + scanResult.level);
                    adapter.notifyDataSetChanged();
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
                            printConsole("distance 1 :" + distance1);
                            printConsole("distance 2 :" + distance2);
                            printConsole("distance 3 :" + distance3);

                        }
                    });
                    //======================================================================
                    //calculate the coordinate
                    //======================================================================


                }

                sleep(500);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        printConsole("--------------------- ");
                    }
                });
            }
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    printConsole("scanning done; Current data: " + results_all.size());
                    registerReceiver(wifiReceiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
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
