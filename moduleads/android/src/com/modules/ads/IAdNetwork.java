package com.modules.ads;

import android.app.Activity;
import android.content.Intent;
import android.os.Handler;

import org.json.JSONObject;

public abstract class IAdNetwork {

    // IMPORTANT: Do not change the sequence of enum here
    public enum AdType{
        VIDEO(0),
        INTERSTITIAL(1),
        BANNER(2),
        APPOPEN(3);

        private final int value;

        AdType(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }

    public enum AdFailEvent{
        PLAY(0),
        LOAD(1);

        private final int value;

        AdFailEvent(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }

    public enum AdCacheStatus{
        NOTCACHED(0),
        INPROGRESS(1),
        CACHED(2);

        private final int value;

        AdCacheStatus(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }

    public interface Listener {
        public void onAdsSDKInitialized(IAdNetwork network);

        public void onAdLoaded(IAdNetwork network);

        public void onAdFailed(IAdNetwork network, final AdType adType, AdFailEvent eventType);

        public void onAdClosed(IAdNetwork network, final AdType adType, final JSONObject data);

        public void onAdStarted(IAdNetwork network, final AdType adType);
    }

    public class AdNetworkAdTypeNotSupported extends Exception {
        public AdNetworkAdTypeNotSupported(IAdNetwork network, String adType) {
            super(String.format("%s doesn't support %s. Implement it or never call!", network.getName(), adType));
        }
    }

    public class Size {
        private float mWidth = 0.f;
        private float mHeight = 0.f;

        public Size(float width, float height) {
            mWidth = width;
            mHeight = height;
        }

        public final float getWidth() {
            return mWidth;
        }

        public void setWidth(final float width) {
            mWidth = width;
        }

        public final float getHeight() {
            return mHeight;
        }

        public void setHeight(final float height) {
            mHeight = height;
        }
    }

    protected Activity mActivity;
    protected IAdNetwork.Listener mListener = null;
    private String mName = null;
    private float bannerAdReCasheInterval = 30.0f;

    public final void setListener(IAdNetwork.Listener listener) {
        mListener = listener;
    }

    public final IAdNetwork.Listener getListener() {
        return mListener;
    }

    protected IAdNetwork(Activity pActivity, IAdNetwork.Listener listener, final String networkName) {
        mName = networkName;
        mActivity = pActivity;
        mListener = listener;
    }

    final public String getName() {
        return mName;
    }

    public void showRewardedAd() throws AdNetworkAdTypeNotSupported {
        throw new AdNetworkAdTypeNotSupported(this, "VIDEO");
    }

    public void showInterstitialAd() throws AdNetworkAdTypeNotSupported {
        throw new AdNetworkAdTypeNotSupported(this, "INTERSTITIAL");
    }

    public void showBannerAd() throws AdNetworkAdTypeNotSupported {
        throw new AdNetworkAdTypeNotSupported(this, "BANNER");
    }

    public void hideBannerAd() throws AdNetworkAdTypeNotSupported {
        throw new AdNetworkAdTypeNotSupported(this, "BANNER");
    }

    public IAdNetwork.Size getBannerSize() {
        return new IAdNetwork.Size(0, 0);
    }

    public void showAppOpenAd() throws AdNetworkAdTypeNotSupported {
        throw new AdNetworkAdTypeNotSupported(this, "APPOPEN");
    }
    public boolean isRewardedAdAvailable() {
        return false;
    }

    public void tryCacheAds(final AdType adType, final AdFailEvent eventType)
    {
        if (eventType == AdFailEvent.LOAD) {
            final long milliSecDelayTime;
            final int adReCasheIntervalMultiplyer = 2;
            switch (adType) {
                case BANNER:
                    milliSecDelayTime = (long)(bannerAdReCasheInterval * 1000);
                    mActivity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            final Handler handler = new Handler();
                            handler.postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    if (!isBannerAdAvailable()) {
                                        bannerAdReCasheInterval *= adReCasheIntervalMultiplyer;
                                        tryCacheBannerAd();
                                    }
                                }
                            }, milliSecDelayTime);
                        }
                    });
                    break;
                default:
                    break;
            }
        }
    }

    public void tryCacheBannerAd() { }

    public boolean isInterstitialAdAvailable() {
        return false;
    }

    public boolean isBannerAdAvailable() {
        return false;
    }

    public boolean isAppOpenAdAvailable() {
        return false;
    }

    protected final void notifyListenerOnAdsSDKInitialized() {
        if (mListener != null) {
            mListener.onAdsSDKInitialized(this);
        }
    }

    protected final void notifyListenerOnAdLoaded() {
        if (mListener != null) {
            mListener.onAdLoaded(this);
        }
    }

    protected final void notifyListenerOnAdClosed(final AdType adType, final JSONObject data) {
        if (mListener != null) {
            mListener.onAdClosed(this, adType, data);
        }
    }

    protected final void notifyListenerOnAdFailed(final AdType adType, final AdFailEvent eventType) {
        if (mListener != null) {
            mListener.onAdFailed(this, adType, eventType);
        }
    }

    protected final void notifyListenerOnAdStarted(final AdType adType) {
        if (mListener != null) {
            mListener.onAdStarted(this, adType);
        }
    }

    public void onStart() {
    }

    public void onStop() {
    }

    public void onPause() {
    }

    public void onResume() {
    }

    public void onDestroy() {
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
    }
}
