package com.modules.common;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Environment;
import android.os.StatFs;
import android.provider.Settings.Secure;
import android.telephony.TelephonyManager;
import android.util.Log;

import com.easyndk.classes.AndroidNDKHelper;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;

import org.json.JSONObject;

import java.io.File;

///
public class CommonModuleUtils extends Activity {
    static private final String TAG = CommonModuleUtils.class.getSimpleName();

    private static final long MEGA_BYTE = 1048576L;

    static public int getIdentifierFromDrawable(String key)
    {
        return ModuleCommon._context.getResources().getIdentifier (key,"drawable",ModuleCommon._context.getApplicationContext().getPackageName());
    }
    static public int getIdentifierFromString(String key)
    {
        return ModuleCommon._context.getResources().getIdentifier (key,"string",ModuleCommon._context.getApplicationContext().getPackageName());
    }

    public static String getDeviceManufacturer()
    {
    	String deviceManufacturer = android.os.Build.MANUFACTURER;
    	return deviceManufacturer;
    }

    public static String getDeviceModel()
    {
    	String deviceModel = android.os.Build.MODEL;
    	return deviceModel;
    }
    
    public static String getDeviceOSVersion()
    {
    	String deviceOS = android.os.Build.VERSION.RELEASE;
    	return deviceOS;
    }

    public static String getDeviceVersion()
    {
        final PackageManager packageManager = ModuleCommon._context.getPackageManager();
        PackageInfo packageInfo;
        try {
            packageInfo = packageManager.getPackageInfo(ModuleCommon._context.getPackageName(),0);
        } catch (final PackageManager.NameNotFoundException e) {
            packageInfo = null;
        }
        final String versionName = (String) (packageInfo != null ? packageInfo.versionName : "(unknown)");
        return versionName;
    }

    public static String getApplicationPackageName()
    {
        return ModuleCommon._context.getPackageName();
    }

    public static String getUniqueIdentifier()
    {
        String deviceId = Secure.getString(ModuleCommon._context.getContentResolver(), Secure.ANDROID_ID);
        return deviceId;
    }

    public String getDeviceUniqueIdentifier()
    {
        return getUniqueIdentifier();
    }

    public static boolean isGooglePlayServicesAvailable()
    {
        final int status = GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(ModuleCommon._context);
        if (status != ConnectionResult.SUCCESS) {
            Log.e(TAG, GoogleApiAvailability.getInstance().getErrorString(status));
            return false;
        } else {
            Log.i(TAG, GoogleApiAvailability.getInstance().getErrorString(status));
            return true;
        }
    }
    
    static public String getApplicationName()
    {
        final PackageManager pm = ModuleCommon._context.getPackageManager();
        ApplicationInfo ai;
        try {
            ai = pm.getApplicationInfo( ModuleCommon._context.getPackageName(), 0);
        } catch (final PackageManager.NameNotFoundException e) {
            ai = null;
        }
        final String applicationName = (String) (ai != null ? pm.getApplicationLabel(ai) : "(unknown)");
        return applicationName;
    }
    
    public static boolean isConnectedToInternet()
    {
        // Note:: This always returns true on BlueStack.
        Context context = ModuleCommon._context;
        ConnectivityManager cm = (ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
        
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        boolean isConnected = activeNetwork != null && activeNetwork.isConnected();

        return isConnected;
    }

    public static int getNetworkType()
    {
        try
        {
            ConnectivityManager mConnectivity = (ConnectivityManager) ModuleCommon._context.getSystemService(Context.CONNECTIVITY_SERVICE);
            TelephonyManager mTelephony = (TelephonyManager) ModuleCommon._context.getSystemService(Context.TELEPHONY_SERVICE);;
            NetworkInfo info = mConnectivity.getActiveNetworkInfo();
            if (info == null || !mConnectivity.getBackgroundDataSetting()) {
                return 2;
            }

            int netType = info.getType();
            int netSubtype = info.getSubtype();
            if (netType == ConnectivityManager.TYPE_WIFI)
            {
                if(info.isConnected())
                {
                    return 1;
                }
            }
            else if (netType == ConnectivityManager.TYPE_MOBILE
                    && netSubtype == TelephonyManager.NETWORK_TYPE_UMTS
                    && !mTelephony.isNetworkRoaming())
            {
                if(info.isConnected())
                {
                    return 0;
                }
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        return 2;
    }

    public static void SendMessageWithParametersInGLThread(final String functionName, final JSONObject parameters)
    {
        ((ModuleCommon)ModuleCommon._context).runOnGLThread(new Runnable()
        {
            public void run()
            {
                AndroidNDKHelper.SendMessageWithParameters(functionName, parameters);
            }
        });
    }

    // storage related fucntions

    public static int getGameSize()
    {
        long totalSize = 0;
        File appBaseFolder = ModuleCommon._context.getFilesDir().getParentFile();
        File appExternalFolder = ModuleCommon._context.getExternalCacheDir().getParentFile();
        for (File f: appBaseFolder.listFiles()) {
            if (f.isDirectory()) {
                long dirSize = getFolderSize(f);
                totalSize += dirSize;
            } else {
                totalSize += f.length();
            }
        }

        for (File f: appExternalFolder.listFiles()) {
            if (f.isDirectory()) {
                long dirSize = getFolderSize(f);
                totalSize += dirSize;
            } else {
                totalSize += f.length();
            }
        }
        return (int) (totalSize/MEGA_BYTE);
    }

    private static long getFolderSize(File folderPath)
    {
        long totalSize = 0;

        if (folderPath == null) {
            return 0;
        }

        if (!folderPath.isDirectory()) {
            return 0;
        }

        File[] files = folderPath.listFiles();
        for (File file : files) {
            if (file.isFile()) {
                totalSize += file.length();
            } else if (file.isDirectory()) {
                totalSize += file.length();
                totalSize += getFolderSize(file);
            }
        }

        return totalSize;
    }

    public static int getTotalDiskSpace()
    {
        StatFs statFs = getStats();
        long   total  = (long)(statFs.getBlockCount()) * (long)(statFs.getBlockSize());
        return (int) (total/MEGA_BYTE);
    }

    public static int getFreeDiskSpace()
    {
        StatFs statFs = getStats();
        long   free   = (long)(statFs.getAvailableBlocks()) * (long)(statFs.getBlockSize());
        return (int) (free/MEGA_BYTE);
    }

    private static boolean externalDiskAvailable()
    {
        return android.os.Environment.getExternalStorageState().equals(android.os.Environment.MEDIA_MOUNTED);
    }

    private static StatFs getStats()
    {
        String path;
        boolean isExternalStorageAvailable = externalDiskAvailable();
        if (isExternalStorageAvailable){
            path = Environment.getExternalStorageDirectory().getAbsolutePath();
        }
        else{
            path = Environment.getRootDirectory().getAbsolutePath();
        }

        return new StatFs(path);
    }

    public static long getHeapMemoryStatus()
    {
        final Runtime runtime = Runtime.getRuntime();
        final long usedMemInMB = (runtime.totalMemory() - runtime.freeMemory()) / 1048576L;
        final long maxHeapSizeInMB = runtime.maxMemory() / 1048576L;
        final long availHeapSizeInMB = maxHeapSizeInMB - usedMemInMB;

        return availHeapSizeInMB;
    }

    public static long getRamMemoryStatus()
    {
        ActivityManager.MemoryInfo memInfo = new ActivityManager.MemoryInfo();
        Context context = ModuleCommon._context;
        ActivityManager activityManager = (ActivityManager)context.getSystemService(ACTIVITY_SERVICE);
        activityManager.getMemoryInfo(memInfo);
        final long availableRamInMB = memInfo.availMem / 1048576L;

        return availableRamInMB;
    }

    public static long getTotalRamMemoryStatus()
    {
        ActivityManager.MemoryInfo memInfo = new ActivityManager.MemoryInfo();
        Context context = ModuleCommon._context;
        ActivityManager activityManager = (ActivityManager)context.getSystemService(ACTIVITY_SERVICE);
        activityManager.getMemoryInfo(memInfo);
        final long availableRamInMB = memInfo.totalMem / 1048576L;

        return availableRamInMB;
    }
}
