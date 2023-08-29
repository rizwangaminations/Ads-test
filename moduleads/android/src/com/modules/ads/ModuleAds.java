package com.modules.ads;

import android.content.Intent;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;

import com.easyndk.classes.AndroidNDKHelper;
import com.modules.common.CommonModuleUtils;
import com.modules.common.LogWrapper;
import com.modules.common.ModuleCommon;

import org.json.JSONException;
import org.json.JSONObject;

public class ModuleAds implements IAdNetwork.Listener {
    private static final String TAG = ModuleAds.class.getSimpleName();

    static private ModuleAds moduleAds = null;
    private Handler mAdsHandler = null;
    private Handler mCacheHandler = null;
    private Runnable checkCacheStatusCode = null;
    private AppLovinSetup mAppLovinNetwork = null;

    public void initialize() {
        LogWrapper.d(TAG, "initialize");
        AndroidNDKHelper.AddNDKReceiver(this, "ndk-receiver-ads-module");
        moduleAds = this;
    }

    public void ___initSDKs___(JSONObject params) throws JSONException{
        final ModuleAds finalThis = this;
        (ModuleCommon._context).runOnUiThread(new Runnable()
        {
            @Override
            public void run() {
                try {
                    mAdsHandler = new Handler(Looper.getMainLooper()) {
                        @Override
                        public void handleMessage(Message msg) {
                            super.handleMessage(msg);
                            mAppLovinNetwork = new AppLovinSetup(ModuleCommon._context, finalThis);
                        }
                    };
                    mAdsHandler.sendEmptyMessage(0);
                } catch (Exception e) {
                    e.printStackTrace();
                    LogWrapper.e(TAG, e.getLocalizedMessage());
                }
            }
        });
    }

    public void ___preLoadAds___(final JSONObject params) throws JSONException{
        final ModuleAds finalThis = this;
        (ModuleCommon._context).runOnUiThread(new Runnable()
        {
            @Override
            public void run() {
                try {
                    mAdsHandler = new Handler(Looper.getMainLooper()) {
                        @Override
                        public void handleMessage(Message msg) {
                            super.handleMessage(msg);
                            mAppLovinNetwork.preLoadAds(params);
                        }
                    };
                    mAdsHandler.sendEmptyMessage(0);
                } catch (Exception e) {
                    e.printStackTrace();
                    LogWrapper.e(TAG, e.getLocalizedMessage());
                }
            }
        });
    }

    public void ___updateAdsCacheStatus___(JSONObject params) {
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                JSONObject jsonObject = new JSONObject();
                try {
                    final String networkName = "AppLovin";
                    jsonObject.put(networkName + "Video", mAppLovinNetwork.isRewardedAdAvailable());
                    jsonObject.put(networkName + "Interstitial", mAppLovinNetwork.isInterstitialAdAvailable());
                    jsonObject.put(networkName + "AppOpen", mAppLovinNetwork.isAppOpenAdAvailable());
                    //BannerAd information json node
                    if (mAppLovinNetwork.isBannerAdAvailable()) {
                        JSONObject bannerParams = new JSONObject();
                        bannerParams.put("cached", true);
                        final IAdNetwork.Size bannerSize = mAppLovinNetwork.getBannerSize();
                        bannerParams.put("width", bannerSize.getWidth());
                        bannerParams.put("height", bannerSize.getHeight());
                        jsonObject.put(networkName + "Banner", bannerParams);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                LogWrapper.d(TAG, "Sending ads status to GL thread.");
                CommonModuleUtils.SendMessageWithParametersInGLThread("setAdsCacheStatus", jsonObject);
            }
        });
    }

    public void ___showInterstitialAd___(JSONObject params) throws JSONException {
        final JSONObject finalParams = params;
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (mAppLovinNetwork != null) {
                    mAppLovinNetwork.showInterstitialAd();
                }
            }
        });
    }

    public void ___showRewardedAd___(JSONObject params) throws JSONException {
        final JSONObject finalParams = params;
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.currentThread().setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
                        public void uncaughtException(Thread t, Throwable e) {
                            e.printStackTrace();
                            LogWrapper.e(TAG, e.getLocalizedMessage());
                            System.out.println("Rob_Uncaught_exception");
                            JSONObject message = new JSONObject();
                            AndroidNDKHelper.SendMessageWithParameters("sendGameAnalyticsWarning", message);
                        }
                    });

                    if (mAppLovinNetwork != null) {
                        mAppLovinNetwork.showRewardedAd();
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                    LogWrapper.e(TAG, e.getLocalizedMessage());
                }
            }
        });
    }

    public void ___showBannerAd___(JSONObject params) throws JSONException {
        final JSONObject finalParams = params;
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (mAppLovinNetwork != null) {
                    mAppLovinNetwork.showBannerAd();
                }
            }
        });
    }

    public void ___hideBannerAd___(JSONObject params) throws JSONException {
        final JSONObject finalParams = params;
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (mAppLovinNetwork != null) {
                    mAppLovinNetwork.hideBannerAd();
                }
            }
        });
    }

    public void ___showAppOpenAd___(JSONObject params) throws JSONException {
        final JSONObject finalParams = params;
        (ModuleCommon._context).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (mAppLovinNetwork != null) {
                    mAppLovinNetwork.showAppOpenAd();
                }
            }
        });
    }

    public static void onStart() {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onStart();
        }
    }

    public static void onStop() {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onStop();
        }
    }

    public static void onResume() {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onResume();
        }
    }

    public static void onPause() {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onPause();
        }
    }

    public static void onDestroy() {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onDestroy();
        }
    }

    public static void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (moduleAds != null) {
            moduleAds.mAppLovinNetwork.onActivityResult(requestCode, resultCode, data);
        }
    }

    //NOTE: IAdNetwork.Listener overrides. Cache status should be updated once Ad loaded, failed or played

    @Override
    public void onAdsSDKInitialized(IAdNetwork network) {
        LogWrapper.i(TAG, String.format("onAdsSDKInitialized(%s)", network.getName()));
        JSONObject jsonObject = new JSONObject();
        this.onAdsSDKInitialized(jsonObject);
    }

    @Override
    public void onAdLoaded(IAdNetwork network) {
        LogWrapper.i(TAG, String.format("onAdLoaded(%s)", network.getName()));
        this.___updateAdsCacheStatus___(null);
    }

    @Override
    public void onAdFailed(IAdNetwork network, final IAdNetwork.AdType adType, IAdNetwork.AdFailEvent eventType) {
        LogWrapper.i(TAG, String.format("onAdFailed(%s, %s)", network.getName(), adType.toString()));
        // Remove this if condition once Load fail also needs to be handled at C++ end
        if (eventType == IAdNetwork.AdFailEvent.PLAY) {
            JSONObject jsonObject = new JSONObject();
            try {
                if (adType == IAdNetwork.AdType.VIDEO || adType == IAdNetwork.AdType.INTERSTITIAL || adType == IAdNetwork.AdType.APPOPEN) {
                    jsonObject.put("adType", adType.getValue());
                    jsonObject.put("failEvent", eventType.getValue());
                    adFailedCallback(jsonObject);
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        this.___updateAdsCacheStatus___(null);
    }

    @Override
    public void onAdClosed(IAdNetwork network, final IAdNetwork.AdType adType, final JSONObject jsonObject) {
        try {
            LogWrapper.i(TAG, String.format("onAdClosed(%s, %s, completed=%b)", jsonObject.getString("networkName"), jsonObject.getString("adType"), jsonObject.getBoolean("giveReward")));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        adClosedCallback(jsonObject);
        this.___updateAdsCacheStatus___(null);
    }

    @Override
    public void onAdStarted(IAdNetwork network, final IAdNetwork.AdType adType) {
        LogWrapper.i(TAG, String.format("onAdStarted(%s, %s)", network.getName(), adType.toString()));
        JSONObject jsonObject = new JSONObject();
        try {
            if (adType == IAdNetwork.AdType.VIDEO || adType == IAdNetwork.AdType.INTERSTITIAL || adType == IAdNetwork.AdType.APPOPEN) {
                jsonObject.put("adType", adType.getValue());
                adStartedCallback(jsonObject);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void onAdsSDKInitialized(final JSONObject params) {
        ((ModuleCommon) ModuleCommon._context).runOnGLThread(new Runnable() {
            @Override
            public void run() {
                AndroidNDKHelper.SendMessageWithParameters("onAdsSDKInitializedCallback", params);
            }
        });
    }

    private void adClosedCallback(final JSONObject params) {
        ((ModuleCommon) ModuleCommon._context).runOnGLThread(new Runnable() {
            @Override
            public void run() {
                AndroidNDKHelper.SendMessageWithParameters("adClosedCallback", params);
            }
        });
    }

    private void adStartedCallback(final JSONObject params) {
        ((ModuleCommon) ModuleCommon._context).runOnGLThread(new Runnable() {
            @Override
            public void run() {
                AndroidNDKHelper.SendMessageWithParameters("adStartedCallback", params);
            }
        });
    }

    private void adFailedCallback(final JSONObject params) {
        ((ModuleCommon) ModuleCommon._context).runOnGLThread(new Runnable() {
            @Override
            public void run() {
                AndroidNDKHelper.SendMessageWithParameters("adFailedCallback", params);
            }
        });
    }
}