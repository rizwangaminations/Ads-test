
package com.modules.ads;

import android.app.Activity;
import android.content.Context;
import android.content.pm.ActivityInfo;
import android.graphics.Color;
import android.os.Handler;
import android.util.DisplayMetrics;
import android.view.Display;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;

import com.applovin.mediation.MaxAd;
import com.applovin.mediation.MaxAdListener;
import com.applovin.mediation.MaxAdViewAdListener;
import com.applovin.mediation.MaxError;
import com.applovin.mediation.MaxReward;
import com.applovin.mediation.MaxRewardedAdListener;
import com.applovin.mediation.ads.MaxAdView;
import com.applovin.mediation.ads.MaxInterstitialAd;
import com.applovin.mediation.ads.MaxRewardedAd;
import com.applovin.mediation.ads.MaxAppOpenAd;
import com.applovin.sdk.AppLovinPrivacySettings;
import com.applovin.sdk.AppLovinSdk;
import com.applovin.sdk.AppLovinSdkConfiguration;
import com.applovin.sdk.AppLovinSdkSettings;
import com.applovin.sdk.AppLovinSdkUtils;
import com.modules.common.LogWrapper;
import com.modules.common.ModuleCommon;
import com.facebook.ads.AdSettings;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.TimeUnit;

    public class AppLovinSetup extends IAdNetwork{
        private final String TAG = com.modules.ads.AppLovinSetup.class.getSimpleName();
        private FrameLayout mCocos2dFrameLayout = null;
        private AppLovinSdk m_applovinSDK;
        private MaxInterstitialAd m_interstitialAdDelegate;
        private MaxRewardedAd m_rewardedAdDelegate;
        private MaxAdView m_bannerAdDelegate;
        private MaxAppOpenAd m_appOpenAdDelegate;
        private boolean m_rewardedAdCompleted = false;
        private boolean mIsBannerAdLoaded = false;
        private int     m_interstitialAdRetryAttempt = 0;
        private int     m_rewardedAdRetryAttempt = 0;
        private int     m_appOpenAdRetryAttempt = 0;

            private final String maxInterstitialID = "cf895d9d45e59c24";
            private final String maxRewardedVideoID = "7d1bc6ba60be7a86";
            private final String maxBannerID = "245f19d28444b55f";
            private final String maxAppOpenID = "c5972fad2e4973f6";

            private final String applovinSDKKey = "EqLbSV6MqFggiNVy67J0kNSz8QUgtEr62BiVgpsV3XAnvfi_o10VOSTWuyCmB1sEDTluMbOP7TA0Du00v1VHUz";



        public static final String NETWORK_NAME = "AppLovin";

        public AppLovinSetup(Activity pActivity, IAdNetwork.Listener listener) {
            super(pActivity, listener, NETWORK_NAME);
            AppLovinSdkSettings userSettings = new AppLovinSdkSettings(ModuleCommon._context );
            mCocos2dFrameLayout = ModuleCommon.getCocos2dxFrameLayout();
            updateUserConsent();
            AdSettings.setDataProcessingOptions( new String[] {} );
            m_applovinSDK= AppLovinSdk.getInstance(applovinSDKKey, userSettings, ModuleCommon._context );
            m_applovinSDK.getSettings().setMuted(false);
            m_applovinSDK.setMediationProvider( "max" );
            m_applovinSDK.initializeSdk(new AppLovinSdk.SdkInitializationListener() {
                @Override
                public void onSdkInitialized(final AppLovinSdkConfiguration configuration)
                {
                    ModuleCommon._context .runOnUiThread(new Runnable() {
                        @Override
                        public void run()
                        {
                            createRewardedAdDelegate();
                            createInterstitialAdDelegate();
                            createBannerAdDelegate();
                            createAppOpenAdDelegate();
                            notifyListenerOnAdsSDKInitialized();
                            if (BuildConfig.BUILD_TYPE.toLowerCase().equals("debug")) {
                                m_applovinSDK.showMediationDebugger();
                            }
                        }
                    });
                }
            } );

        }

        void createInterstitialAdDelegate()
        {
            m_interstitialAdDelegate = new MaxInterstitialAd( maxInterstitialID, m_applovinSDK, ModuleCommon._context );
            m_interstitialAdDelegate.setListener(new MaxAdListener() {
                @Override
                public void onAdLoaded(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdLoaded::interstitial");
                    // Interstitial ad is ready to be shown. interstitialAd.isReady() will now return 'true'
                    notifyListenerOnAdLoaded();
                    m_interstitialAdRetryAttempt = 0;
                }

                @Override
                public void onAdLoadFailed(String adUnitId, final MaxError error) {
                    LogWrapper.i(TAG, "onAdLoadFailed::interstitial");
                    m_interstitialAdRetryAttempt++;
                    long delayMillis = TimeUnit.SECONDS.toMillis( (long) Math.pow( 2, Math.min( 6, m_interstitialAdRetryAttempt ) ) );
                    final Handler handler = new Handler();
                    handler.postDelayed( new Runnable()
                    {
                        @Override
                        public void run()
                        {
                            m_interstitialAdDelegate.loadAd();
                        }
                    }, delayMillis );
                }

                @Override
                public void onAdDisplayed(MaxAd ad) {
                    LogWrapper.d(TAG, "interstitial adDisplayed");
                    String crashlyticsLog = ad.getNetworkName() + " Interstitial ad shown via applovin mediation";

                    notifyListenerOnAdStarted(AdType.INTERSTITIAL);
                }

                @Override
                public void onAdHidden(MaxAd ad) {
                    // Interstitial ad is hidden. Pre-load the next ad
                    LogWrapper.e(TAG, "interstitial adHidden");

                    double revenue = ad.getRevenue();
                    String networkName = ad.getNetworkName();
                    boolean completed = true;
                    AdType adType = AdType.INTERSTITIAL;

                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("adType", adType.getValue());
                        jsonObject.put("giveReward", completed);
                        jsonObject.put("networkName", networkName);
                        jsonObject.put("revenue", revenue);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    notifyListenerOnAdClosed(AdType.INTERSTITIAL, jsonObject);
                    m_interstitialAdDelegate.loadAd();
                }

                @Override
                public void onAdClicked(MaxAd ad) {

                }

                @Override
                public void onAdDisplayFailed(MaxAd ad, final MaxError error) {
                    // Interstitial ad failed to display. We recommend loading the next ad
                    notifyListenerOnAdFailed(AdType.INTERSTITIAL, AdFailEvent.PLAY);
                    m_interstitialAdDelegate.loadAd();
                }
            });
        }

        void createRewardedAdDelegate()
        {
            m_rewardedAdDelegate = MaxRewardedAd.getInstance( maxRewardedVideoID, m_applovinSDK, ModuleCommon._context );
            m_rewardedAdDelegate.setListener(new MaxRewardedAdListener() {
                @Override
                public void onRewardedVideoStarted(MaxAd ad) {

                }

                @Override
                public void onRewardedVideoCompleted(MaxAd ad) {

                    LogWrapper.i(TAG, "onRewardedVideoCompleted");
                }

                @Override
                public void onUserRewarded(MaxAd ad, MaxReward reward) {

                    m_rewardedAdCompleted = true;
                    LogWrapper.i(TAG, "onUserRewarded");
                }

                @Override
                public void onAdLoaded(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdLoaded::rewarded");
                    notifyListenerOnAdLoaded();
                    m_rewardedAdRetryAttempt = 0;
                }

                @Override
                public void onAdLoadFailed(String adUnitId, final MaxError error) {
                    LogWrapper.i(TAG, "onAdLoadFailed::rewarded");

                    m_rewardedAdRetryAttempt++;
                    long delayMillis = TimeUnit.SECONDS.toMillis( (long) Math.pow( 2, Math.min( 6, m_rewardedAdRetryAttempt ) ) );
                    final Handler handler = new Handler();
                    handler.postDelayed( new Runnable()
                    {
                        @Override
                        public void run()
                        {
                            m_rewardedAdDelegate.loadAd();
                        }
                    }, m_rewardedAdRetryAttempt );
                }

                @Override
                public void onAdDisplayed(MaxAd ad) {
                    String crashlyticsLog = ad.getNetworkName() + " Video ad shown via applovin mediation";

                    notifyListenerOnAdStarted(AdType.VIDEO);
                    LogWrapper.d(TAG, "VideoAds::APPLOVIN adDisplayed");
                }

                @Override
                public void onAdHidden(MaxAd ad) {

                    double revenue = ad.getRevenue();
                    String networkName = ad.getNetworkName();
                    boolean completed = m_rewardedAdCompleted;
                    AdType adType = AdType.VIDEO;
                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("adType", adType.getValue());
                        jsonObject.put("giveReward", completed);
                        jsonObject.put("networkName", networkName);
                        jsonObject.put("revenue", revenue);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    notifyListenerOnAdClosed(AdType.VIDEO, jsonObject);
                    m_rewardedAdDelegate.loadAd();
                }

                @Override
                public void onAdClicked(MaxAd ad) {

                }

                @Override
                public void onAdDisplayFailed(MaxAd ad, final MaxError error) {
                    // Rewarded ad failed to display. We recommend loading the next ad
                    m_rewardedAdDelegate.loadAd();
                }
            });
        }


        void createBannerAdDelegate()
        {
            m_bannerAdDelegate = new MaxAdView( maxBannerID, m_applovinSDK, ModuleCommon._context );
            m_bannerAdDelegate.setListener(new MaxAdViewAdListener() {
                @Override
                public void onAdExpanded(MaxAd ad) {
                    LogWrapper.d(TAG, "onAdExpanded::Banner");
                }

                @Override
                public void onAdCollapsed(MaxAd ad) {
                    LogWrapper.d(TAG, "onAdCollapsed::Banner");
                }

                @Override
                public void onAdLoaded(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdLoaded::Banner");
                    if (m_bannerAdDelegate.getVisibility() == View.INVISIBLE)
                    {
                        m_bannerAdDelegate.stopAutoRefresh();
                    }
                    mIsBannerAdLoaded = true;
                    notifyListenerOnAdLoaded();
                }

                @Override
                public void onAdLoadFailed(String adUnitId, final MaxError error) {
                    LogWrapper.i(TAG, "onAdLoadFailed::Banner");
                    mIsBannerAdLoaded = false;
                    notifyListenerOnAdFailed(AdType.BANNER, AdFailEvent.LOAD);
                }

                @Override
                public void onAdDisplayed(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdDisplayed");
                    String crashlyticsLog = ad.getNetworkName() + " banner ad shown via applovin mediation";

                }

                @Override
                public void onAdHidden(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdHidden::Banner");

                }

                @Override
                public void onAdClicked(MaxAd ad) {

                }

                @Override
                public void onAdDisplayFailed(MaxAd ad, final MaxError error) {
                    LogWrapper.i(TAG, "onAdDisplayFailed::Banner");
                }
            });

            final boolean isTablet = AppLovinSdkUtils.isTablet( ModuleCommon._context ); // Available on Android SDK 9.6.2+
            final int heightPx = AppLovinSdkUtils.dpToPx( ModuleCommon._context, isTablet ? 90 : 50 );
            final FrameLayout.LayoutParams params = new FrameLayout.LayoutParams( ViewGroup.LayoutParams.MATCH_PARENT, heightPx );
            params.gravity = Gravity.BOTTOM|Gravity.CENTER;
            m_bannerAdDelegate.setLayoutParams(params);
            //NOTE: add banner to Cocos2dx mFrameLayout
            mCocos2dFrameLayout.addView(m_bannerAdDelegate);
            m_bannerAdDelegate.setBackgroundColor(Color.TRANSPARENT);
            m_bannerAdDelegate.setVisibility(View.INVISIBLE);
        }

        void createAppOpenAdDelegate()
        {
            m_appOpenAdDelegate = new MaxAppOpenAd( maxAppOpenID, m_applovinSDK );
            m_appOpenAdDelegate.setListener(new MaxAdListener() {
                @Override
                public void onAdLoaded(MaxAd ad) {
                    LogWrapper.i(TAG, "onAdLoaded::appOpen");
                    // AppOpen ad is ready to be shown. appOpenAd.isReady() will now return 'true'
                    notifyListenerOnAdLoaded();
                    m_appOpenAdRetryAttempt = 0;
                }

                @Override
                public void onAdLoadFailed(String adUnitId, final MaxError error) {
                    LogWrapper.i(TAG, "onAdLoadFailed::appOpen");
                    m_appOpenAdRetryAttempt++;
                    long delayMillis = TimeUnit.SECONDS.toMillis( (long) Math.pow( 2, Math.min( 6, m_appOpenAdRetryAttempt ) ) );
                    final Handler handler = new Handler();
                    handler.postDelayed( new Runnable()
                    {
                        @Override
                        public void run()
                        {
                            m_appOpenAdDelegate.loadAd();
                        }
                    }, delayMillis );
                }

                @Override
                public void onAdDisplayed(MaxAd ad) {
                    LogWrapper.d(TAG, "appOpen adDisplayed");
                    String crashlyticsLog = ad.getNetworkName() + " AppOpen ad shown via applovin mediation";

                    notifyListenerOnAdStarted(AdType.APPOPEN);
                }

                @Override
                public void onAdHidden(MaxAd ad) {
                    // AppOpen ad is hidden. Pre-load the next ad
                    LogWrapper.e(TAG, "appOpen adHidden");

                    double revenue = ad.getRevenue();
                    String networkName = ad.getNetworkName();
                    boolean completed = true;
                    AdType adType = AdType.APPOPEN;

                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("adType", adType.getValue());
                        jsonObject.put("giveReward", completed);
                        jsonObject.put("networkName", networkName);
                        jsonObject.put("revenue", revenue);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    notifyListenerOnAdClosed(AdType.APPOPEN, jsonObject);
                    m_appOpenAdDelegate.loadAd();
                }

                @Override
                public void onAdClicked(MaxAd ad) {

                }

                @Override
                public void onAdDisplayFailed(MaxAd ad, final MaxError error) {
                    // AppOpen ad failed to display. We recommend loading the next ad
                    notifyListenerOnAdFailed(AdType.APPOPEN, AdFailEvent.PLAY);
                    m_appOpenAdDelegate.loadAd();
                }
            });
        }

        void preLoadAds(JSONObject params)
        {
            String adTypeKey = params.optString("AdType");
            switch (adTypeKey) {
                case "Interstitial":
                    preLoadInterstitialAd();
                    break;
                case "Video":
                    preLoadRewardedAd();
                    break;
                case "Banner":
                    preLoadBannerAd();
                    break;
                case "AppOpen":
                    preLoadAppOpenAd();
                    break;
            }
        }

        void preLoadInterstitialAd()
        {
            if (!m_interstitialAdDelegate.isReady())
            {
                m_interstitialAdDelegate.loadAd();
            }
        }

        void preLoadRewardedAd()
        {
            if (!m_rewardedAdDelegate.isReady())
            {
                m_rewardedAdDelegate.loadAd();
            }
        }

        void preLoadBannerAd()
        {
            if (!mIsBannerAdLoaded)
            {
                m_bannerAdDelegate.loadAd();
            }
        }

        void preLoadAppOpenAd()
        {
            if (!m_appOpenAdDelegate.isReady())
            {
                m_appOpenAdDelegate.loadAd();
            }
        }

        public void updateUserConsent()
        {
            AppLovinPrivacySettings.setHasUserConsent(true, mActivity);
        }




        void reloadBanner()
        {
            m_bannerAdDelegate.loadAd();
        }

        public static boolean IsTablet(Context context)
        {
            Display display = ((Activity)context).getWindowManager().getDefaultDisplay();
            DisplayMetrics displayMetrics = new DisplayMetrics();
            display.getMetrics(displayMetrics);

            double wInches = displayMetrics.widthPixels / (double)displayMetrics.densityDpi;
            double hInches = displayMetrics.heightPixels / (double)displayMetrics.densityDpi;

            double screenDiagonal = Math.sqrt(Math.pow(wInches, 2) + Math.pow(hInches, 2));
            return (screenDiagonal >= 7.0);
        }

        @Override
        public void showInterstitialAd() {
            if (this.isInterstitialAdAvailable()) {
                m_interstitialAdDelegate.showAd();
            }
            else {
                notifyListenerOnAdFailed(AdType.INTERSTITIAL, AdFailEvent.PLAY);
            }
        }

        @Override
        public void showRewardedAd() {
            m_rewardedAdCompleted = false;
            if (isRewardedAdAvailable()) {
                m_rewardedAdDelegate.showAd();
            } else {
                notifyListenerOnAdFailed(AdType.VIDEO, AdFailEvent.PLAY);
            }
        }

        @Override
        public boolean isInterstitialAdAvailable() {
            return  (m_interstitialAdDelegate != null && m_interstitialAdDelegate.isReady());
        }

        @Override
        public boolean isRewardedAdAvailable() {
            return (m_rewardedAdDelegate != null && m_rewardedAdDelegate.isReady());
        }

        @Override
        public void showBannerAd() {
            if (this.isBannerAdAvailable()) {
                LogWrapper.i(TAG, "Showing applovin banner");
                m_bannerAdDelegate.setVisibility(View.VISIBLE);
                this.mCocos2dFrameLayout.requestLayout();
                this.mCocos2dFrameLayout.invalidate();
                m_bannerAdDelegate.startAutoRefresh();
                LogWrapper.d(TAG, "Start Refresh");
            }
        }

        @Override
        public void hideBannerAd() {
            if (m_bannerAdDelegate != null) {
                //NOTE: show banner view
                LogWrapper.i(TAG, "Hiding applovin banner");
                m_bannerAdDelegate.setVisibility(View.INVISIBLE);
                m_bannerAdDelegate.stopAutoRefresh();
            }
        }

        @Override
        public boolean isBannerAdAvailable() {
            return  (m_bannerAdDelegate != null && mIsBannerAdLoaded);
        }

        @Override
        public void showAppOpenAd() {
            if (this.isAppOpenAdAvailable()) {
                m_appOpenAdDelegate.showAd();
            }
            else {
                notifyListenerOnAdFailed(AdType.APPOPEN, AdFailEvent.PLAY);
            }
        }

        @Override
        public boolean isAppOpenAdAvailable() {
            return  (m_appOpenAdDelegate != null && m_appOpenAdDelegate.isReady());
        }

        @Override
        public final IAdNetwork.Size getBannerSize() {
            if (this.isBannerAdAvailable()) {
                return new IAdNetwork.Size((float) m_bannerAdDelegate.getWidth(), (float) m_bannerAdDelegate.getHeight());
            }
            return new IAdNetwork.Size(0, 0);
        }

        @Override
        public void tryCacheBannerAd() {

            if(!this.isBannerAdAvailable())
            {
                m_bannerAdDelegate.loadAd();
            }
        }

        @Override
        public void onResume() {
            ModuleCommon._context.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER_LANDSCAPE);
        }

    }
