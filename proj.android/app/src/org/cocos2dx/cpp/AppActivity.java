/****************************************************************************
 * Copyright (c) 2008-2010 Ricardo Quesada
 * Copyright (c) 2010-2012 cocos2d-x.org
 * Copyright (c) 2011      Zynga Inc.
 * Copyright (c) 2013-2014 Chukong Technologies Inc.
 * <p>
 * http://www.cocos2d-x.org
 * <p>
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * <p>
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * <p>
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 ****************************************************************************/
package org.cocos2dx.cpp;

import android.content.ComponentCallbacks;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import androidx.multidex.MultiDex;
import android.view.KeyEvent;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.content.pm.PackageManager;
import android.content.pm.PackageInfo;
import com.easyndk.classes.AndroidNDKHelper;
import com.modules.ads.ModuleAds;
import com.modules.common.CommonModuleUtils;
import com.modules.common.LogWrapper;
import com.modules.common.ModuleCommon;

import org.cocos2dx.lib.Cocos2dxHelper;
import org.json.JSONObject;

import java.util.HashMap;
import java.io.File;

public class AppActivity extends ModuleCommon implements ComponentCallbacks {
    private static final String TAG = AppActivity.class.getSimpleName();
    private ImageView splashView;
    private String startLoadingTimeStamp;
    private Thread.UncaughtExceptionHandler mDefaultExceptionHandler;
    private long mUIThreadId;

    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        MultiDex.install(this);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        LogWrapper.d(TAG, "onCreate");
        super.onCreate(savedInstanceState);

        //NOTE: next if statement should be removed when minSdkVersion will be 18 or higher(current = 15)
        if  (Build.VERSION.SDK_INT < Build.VERSION_CODES.JELLY_BEAN_MR2)
        {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);
        }

        long timeMilli = System.currentTimeMillis();
        startLoadingTimeStamp = String.valueOf(timeMilli);
        AndroidNDKHelper.AddNDKReceiver(this, "ndk-receiver-game");

        handleGMSException();
//        initializeCrashlytics();

        String versionName = "";
        if (ModuleCommon._context != null) {
            final PackageManager packageManager = ModuleCommon._context.getPackageManager();
            if (packageManager != null) {
                try {
                    PackageInfo packageInfo = packageManager.getPackageInfo(ModuleCommon._context.getPackageName(), 0);
                    versionName = packageInfo.versionName;
                } catch (PackageManager.NameNotFoundException e) {
                    versionName = null;
                }
            }

            Cocos2dxHelper.setStringForKey("CURRENT_APP_VERSION", versionName);

            createLoadingUI();

            setKeepScreenOn(true);
        }
    }

//    private void initializeCrashlytics()
//    {
//        if (FirebaseCrashlytics.getInstance().didCrashOnPreviousExecution()) {
//            Cocos2dxHelper.setBoolForKey("didGameCrashed", true);
//            Cocos2dxHelper.flush();
//        }
//    }

    private void handleGMSException() {
        mDefaultExceptionHandler = Thread.getDefaultUncaughtExceptionHandler();
        mUIThreadId = Thread.currentThread().getId();
        Thread.setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {

            @Override
            public void uncaughtException(Thread t, Throwable e) {
                if (e != null && t.getId() != mUIThreadId && e.getStackTrace() != null && e.getStackTrace().length > 0
                        && e.getStackTrace()[0].toString().contains("com.google.android.gms")
                        && e.getMessage() != null && e.getMessage().contains("Results have already been set")) {
                    return; // non-UI thread
                }
                if (mDefaultExceptionHandler != null) {
                    mDefaultExceptionHandler.uncaughtException(t, e);
                }
            }

        });
    }

    public void getGameLoadStartTime(JSONObject prms) {
        HashMap<String, String> paramDict = new HashMap<String, String>();
        paramDict.put("gameLoadStartTime", startLoadingTimeStamp);
        JSONObject jsonObject = new JSONObject(paramDict);
        CommonModuleUtils.SendMessageWithParametersInGLThread("getGameLoadStartTime", jsonObject);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        LogWrapper.d(TAG, "onActivityResult" + requestCode + " " + resultCode);
        final int reqCode = requestCode;
        final int resCode = resultCode;
        final Intent intent = data;
        ((ModuleCommon) ModuleCommon._context).runOnGLThread(new Runnable() {
            public void run() {
                ModuleAds.onActivityResult(reqCode, resCode, intent);
            }
        });
    }

    public void initializeAnalytics(JSONObject prms)
    {
        this.runOnUiThread((new Runnable()
        {
            @Override
            public void run()
            {
//                ModuleAnalytics.initializeAnalytics();
            }
        }));
    }

    public void fastInitializeNativeSDKs(JSONObject prms)
    {
        this.runOnUiThread((new Runnable()
        {
            @Override
            public void run()
            {
//                ModuleAnalytics.initializeDeltaDNA();
            }
        }));
    }

    @Override
    protected void onStart() {
        super.onStart();
        LogWrapper.d(TAG, "onStart");
        ModuleAds.onStart();
    }

    @Override
    protected void onStop() {
        ModuleAds.onStop();
        super.onStop();
    }

    @Override
    public boolean dispatchKeyEvent(final KeyEvent pKeyEvent) {
        if (this.getGLSurfaceView() != null && this.getCurrentFocus() != this.getGLSurfaceView()) {
            this.getGLSurfaceView().requestFocus();
        }

        return super.dispatchKeyEvent(pKeyEvent);
    }

    @Override
    protected void onResume() {
        super.onResume();
        LogWrapper.d(TAG, "onResume");
        ModuleAds.onResume();
    }

    @Override
    protected void onPause() {
        ModuleAds.onPause();

        super.onPause();
    }

    @Override
    protected void onDestroy() {
        ModuleAds.onDestroy();
        super.onDestroy();

        AndroidNDKHelper.RemoveNDKReceiver("ndk-receiver-game");
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
    }
}
