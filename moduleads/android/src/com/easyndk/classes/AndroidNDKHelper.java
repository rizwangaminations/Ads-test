package com.easyndk.classes;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;

public class AndroidNDKHelper {

	private static Object callHandler = null;
	private static Handler NDKHelperHandler = null;

	private static native void CPPNativeCallHandler(String json);
	private static String __CALLED_METHOD__ = "calling_method_name";
	private static String __CALLED_METHOD_PARAMS__ = "calling_method_params";
	private final static int __MSG_FROM_CPP__ = 5;
	private static HashMap<String, Object> receivers = new HashMap<String, Object>();

	public static void SetNDKReceiver(Object callReceiver)
	{
		callHandler = callReceiver;
		NDKHelperHandler = new Handler()
		{
			public void handleMessage(Message msg)
			{
				switch(msg.what)
				{
				case __MSG_FROM_CPP__:
					try
					{
						NDKMessage message = (NDKMessage)msg.obj;
						message.methodToCall.invoke(AndroidNDKHelper.callHandler, message.methodParams);
					}
					catch (IllegalArgumentException e)
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					catch (IllegalAccessException e)
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					catch (InvocationTargetException e)
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					break;
				}
			}
		};
	}
	
	public static void AddNDKReceiver(Object callReceiver, final String moduleName)
	{
		receivers.put(moduleName, callReceiver);
	}

	public static void RemoveNDKReceiver(final String moduleName)
	{
		receivers.remove(moduleName);
	}

	public static void RemoveAllNDKReceivers()
	{
		receivers.clear();
	}

	public static void SendMessageWithParameters(String methodToCall, JSONObject paramList)
	{
		JSONObject obj = new JSONObject();
		try
		{
			obj.put(__CALLED_METHOD__, methodToCall);
			obj.put(__CALLED_METHOD_PARAMS__, paramList);
			CPPNativeCallHandler(obj.toString());
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public static void ReceiveCppMessage(String json)
	{
		if (json != null)
		{
			try
			{
				JSONObject obj = new JSONObject(json);
				if (obj.has(__CALLED_METHOD__))
				{
					String methodName = obj.getString(__CALLED_METHOD__);
					JSONObject methodParams = null;

					try
					{
						methodParams = obj.getJSONObject(__CALLED_METHOD_PARAMS__);
					}
					catch (JSONException e)
					{
						// if we are finding trouble in looking for params, params might be null
					}

					try
					{
						String ndkIdentifer = methodParams.get("ndkIdentifier").toString();
						Object receiver = AndroidNDKHelper.receivers.get(ndkIdentifer);
						Method m = receiver.getClass().getMethod(methodName, new Class[] { JSONObject.class });

						NDKMessage message = new NDKMessage();
						message.methodToCall = m;
						message.methodParams = methodParams;


						try {
							message.methodToCall.invoke(receiver, methodParams);
						} catch (IllegalAccessException e) {
							e.printStackTrace();
						} catch (InvocationTargetException e) {
							e.printStackTrace();
						}
					}
					catch (NoSuchMethodException e)
					{
						e.printStackTrace();
					}
					catch (IllegalArgumentException e)
					{
						e.printStackTrace();
					}
					catch (NullPointerException e)
					{
						e.printStackTrace();
					}
				}
			}
			catch (JSONException e)
			{
				e.printStackTrace();
			}
		}
	}
}
