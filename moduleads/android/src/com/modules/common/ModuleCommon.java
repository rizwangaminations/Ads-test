package com.modules.common;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;

import com.easyndk.classes.AndroidNDKHelper;
import com.treebo.internetavailabilitychecker.InternetAvailabilityChecker;
import com.treebo.internetavailabilitychecker.InternetConnectivityListener;

import org.cocos2dx.lib.Cocos2dxActivity;
import org.cocos2dx.lib.Cocos2dxGLSurfaceView;
import org.json.JSONException;
import org.json.JSONObject;

public class ModuleCommon extends Cocos2dxActivity implements InternetConnectivityListener
{
    private static final String TAG = ModuleCommon.class.getSimpleName();
    public static Activity _context;
    public static ModuleCommon activity;
    IModuleCommon test;
    private boolean mDestroyed = false;
    public static boolean IS_AMAZON = false;
    public ProgressBar progressUI;

    public static Activity getActivityContext()
    {
        return _context;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        LogWrapper.setLoggingEnabled(true);
        super.onCreate(savedInstanceState);
        Cocos2dxGLSurfaceView glSurfaceView = getGLSurfaceView();
        if (glSurfaceView == null)
        {
            finishAndRemoveTask();
            return;
        }
        glSurfaceView.setMultipleTouchEnabled(false);
        ModuleCommon._context = this;
        activity = this;
//        Branch.getAutoInstance(this.getApplicationContext());
        InternetAvailabilityChecker.init(this);
        InternetAvailabilityChecker.getInstance().addInternetConnectivityListener(this);
    }

    protected void createLoadingUI()
    {
        final RelativeLayout.LayoutParams lps = new RelativeLayout.LayoutParams(96, 96);
        progressUI = new ProgressBar(this);
        progressUI.setIndeterminate(true);
        progressUI.setVisibility(View.GONE);
        addContentView(progressUI, lps);
    }

    @Override
    public void onInternetConnectivityChanged(boolean isConnected) {
        try {
            JSONObject internetConnectivityResponse = new JSONObject();
            internetConnectivityResponse.put("isInternetConnected", isConnected);
            CommonModuleUtils.SendMessageWithParametersInGLThread("onInternetConnectivityChange", internetConnectivityResponse);
        } catch (Exception e)
        {
            LogWrapper.e(TAG, "Zuluu:: Exception Occurred at onInternetConnectivityChanged");
        }
    }

    @Override
    protected void onResume()
    {
        // TODO Auto-generated method stub
        super.onResume();

    }

    @Override
    protected void onPause()
    {
        // TODO Auto-generated method stub
        super.onPause();

    }

    public final boolean isActivityDestroyed()
    {
        return mDestroyed;
    }

    @Override
    protected void onPostResume()
    {
        super.onPostResume();
        if(isFinishing()){
            finish();
        }
    }

    @Override
    public boolean isFinishing()
    {
        return super.isFinishing() || isActivityDestroyed();
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        mDestroyed = true;
        
        AndroidNDKHelper.RemoveNDKReceiver("ndk-receiver-common-module");
    }

    @Override
    protected void onStart()
    {
        // TODO Auto-generated method stub
        super.onStart();
//        Branch branch = Branch.getInstance();
//
//        branch.initSession(new Branch.BranchUniversalReferralInitListener()
//        {
//            @Override
//            public void onInitFinished(BranchUniversalObject branchUniversalObject, LinkProperties linkProperties, BranchError error)
//            {
//                if (error == null)
//                {
//                    if (branchUniversalObject != null)
//                    {
//                        Map<String, String> params = branchUniversalObject.getMetadata();
//                        JSONObject jsonParams = new JSONObject(params);
//                        CommonModuleUtils.SendMessageWithParametersInGLThread("registerNewRoute", jsonParams);
//                    }
//                }
//                else
//                {
//                    LogWrapper.d(TAG, error.getMessage());
//                }
//            }
//        }, this.getIntent().getData(), this);
    }

    @Override
    public void onNewIntent(Intent intent) {
        this.setIntent(intent);
    }

    @Override
    protected void onStop()
    {
        // TODO Auto-generated method stub
        super.onStop();
    }

    public static void setCurrentActivityContext(IModuleCommon delegate)
    {
        activity.test = delegate;
        activity.test.moduleStart();
    }

    public void initialize()
    {
        LogWrapper.d(TAG, "initialize");
        AndroidNDKHelper.AddNDKReceiver(this, "ndk-receiver-common-module");
        onInternetConnectivityChanged(InternetAvailabilityChecker.getInstance().getCurrentInternetAvailabilityStatus());
    }

    public void testNDKCallBack(JSONObject params)
    {
        LogWrapper.d(TAG, "testNDKCallBack");
        CommonModuleUtils.SendMessageWithParametersInGLThread("testNDKCallBack", params);
    }
    
    public void sendFeedbackByMail(JSONObject params) throws Exception
    {
        final String mailingAddress = params.getString("email");
        final String VIPStatus = params.has("VIPTierName") ? params.getString("VIPTierName") : "";
        final String version = CommonModuleUtils.getDeviceVersion();
        final String deviceName = CommonModuleUtils.getDeviceModel();
        final String osVersion = CommonModuleUtils.getDeviceOSVersion();
        final String userIdentifier = CommonModuleUtils.getUniqueIdentifier();
        String extraText = "Version : " + version + "\n" +
                                 "Device : " + deviceName + "\n" +
                                 "OS : " + osVersion + "\n" +
                                 "Platform : Android" + "\n" +
                                 "User : " + userIdentifier;
        if (VIPStatus != "")
        {
            extraText += "\n" + "VIP Status : " + VIPStatus;
        }

        Intent mailToAction = new Intent(Intent.ACTION_SENDTO);
        mailToAction.setData(Uri.parse("mailto:"));
        mailToAction.putExtra(Intent.EXTRA_EMAIL, new String[] { mailingAddress });
        mailToAction.putExtra(Intent.EXTRA_SUBJECT, CommonModuleUtils.getApplicationName());
        mailToAction.putExtra(Intent.EXTRA_TEXT, extraText);
        _context.startActivity(mailToAction);
        
        JSONObject feedbackResponse = new JSONObject();
        feedbackResponse.put("status", true);
        CommonModuleUtils.SendMessageWithParametersInGLThread("sendFeedbackDoneCB", feedbackResponse);
    }

    public String getDeviceSystemVersion()
    {
        final String versionStr = System.getProperty("os.version");
        return versionStr;
    }

    public static FrameLayout getCocos2dxFrameLayout()
    {
        //NOTE: return FrameLayout from Cocos2dxActivity
        return ModuleCommon.activity.mFrameLayout;
    }

    public void runOnUiThreadSafe(Runnable runnable)
    {
        if (runnable != null && !this.isFinishing())
        {
            super.runOnUiThread(runnable);
        }
    }

    public void showLoadingUI(JSONObject prms)
    {
        int x            = 0;
        int y            = 0;
        int width        = 96;
        int height       = 96;
        int screenHeight = 720;
        try {
            x            = prms.getInt("xPos");
            y            = prms.getInt("yPos");
            width        = prms.getInt("width");
            height       = prms.getInt("height");
            screenHeight = prms.getInt("screenHeight");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        final ProgressBar finalProgressUI = ModuleCommon.activity.progressUI;
        final int _x      = x - width  / 2;
        final int _y      = screenHeight - (y + height / 2);
        final int _width  = width;
        final int _height = height;

        ModuleCommon._context.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                final FrameLayout.LayoutParams lps = new FrameLayout.LayoutParams(_width, _height);
                lps.setMargins(_x, _y, 0, 0);
                finalProgressUI.setLayoutParams(lps);
                finalProgressUI.setVisibility(View.VISIBLE);
            }
        });
    }

    public void removeLoadingUI(JSONObject prms)
    {
        final ProgressBar finalProgressUI = ModuleCommon.activity.progressUI;
        ModuleCommon._context.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                finalProgressUI.setVisibility(View.INVISIBLE);
            }
        });
    }

    public void setLoadingUIProgress(JSONObject prms) {
        // NOTE: Function is left empty because the ProgressBar type is currently indeterminate
        // NOTE: Use this function to update the ProgressBar's progress when not set to indeterminate
        /*
        int progress = 0;
        try {
            progress = prms.getInt("progress");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        final int _progress = progress;
        final ProgressBar finalProgressBar = ModuleCommon.activity.progressUI;
        ModuleCommon._context.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                finalProgressBar.setProgress(_progress);
            }
        });
        */
    }

    public void showWebView(JSONObject params) throws Exception
    {

    }
}