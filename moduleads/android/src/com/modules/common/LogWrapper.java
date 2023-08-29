package com.modules.common;

import android.util.Log;

public class LogWrapper 
{
	private static final String TAG = LogWrapper.class.getSimpleName();
	private static final String EMPTY = "";
	private static boolean isLoggingEnabled = true;

	public static void setLoggingEnabled(boolean isEnabled)
	{
		isLoggingEnabled = isEnabled;
	}
	
	/**
	 * Send a VERBOSE log message.
	 * @param tag
	 * @param format
	 * @param args
	 * @return
	 */
	public static int v(String tag, String format, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.v(tag, format(format, args));
		}
		return 0;
	}

	/**
	 * Send a VERBOSE log message and log the exception.
	 * @param tag
	 * @param msg
	 * @param e
	 * @return
	 */
	public static int v(String tag, String msg, Throwable e) 
	{
		if (isLoggingEnabled)
		{
			return Log.v(tag, msg, e);
		}
		return 0;
	}

	/**
	 * Send a VERBOSE log message and log the exception.
	 * @param tag
	 * @param format
	 * @param e
	 * @param args
	 * @return
	 */
	public static int v(String tag, String format, Throwable e, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.v(tag, format(format, args), e);
		}
		return 0;
	}

	/**
	 * Send a DEBUG log message.
	 * @param tag
	 * @param format
	 * @param args
	 * @return
	 */
	public static int d(String tag, String format, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.d(tag, format(format, args));
		}
		return 0;
	}

	/**
	 * Send a DEBUG log message and log the exception.
	 * @param tag
	 * @param msg
	 * @param e
	 * @return
	 */
	public static int d(String tag, String msg, Throwable e) 
	{
		if(isLoggingEnabled)
		{
			return Log.d(tag, msg, e);
		}
		return 0;
	}

	/**
	 * Send a DEBUG log message and log the exception.
	 * @param tag
	 * @param format
	 * @param e
	 * @param args
	 * @return
	 */
	public static int d(String tag, String format, Throwable e, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.d(tag, format(format, args), e);
		}
		return 0;
	}

	/**
	 * Send a WARN log message.
	 * @param tag
	 * @param format
	 * @param args
	 * @return
	 */
	public static int w(String tag, String format, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.w(tag, format(format, args));
		}
		return 0;
	}

	/**
	 * Send a WARN log message and log the exception.
	 * @param tag
	 * @param msg
	 * @param e
	 * @return
	 */
	public static int w(String tag, String msg, Throwable e) 
	{
		if (isLoggingEnabled)
		{
			return Log.w(tag, msg, e);
		}
		return 0;
	}

	/**
	 * Send a WARN log message and log the exception.
	 * @param tag
	 * @param format
	 * @param e
	 * @param args
	 * @return
	 */
	public static int w(String tag, String format, Throwable e, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.w(tag, format(format, args), e);
		}
		return 0;
	}

	/**
	 * Send a INFO log message.
	 * @param tag
	 * @param format
	 * @param args
	 * @return
	 */
	public static int i(String tag, String format, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.i(tag, format(format, args));
		}
		return 0;
	}

	/**
	 * Send a INFO log message and log the exception.
	 * @param tag
	 * @param msg
	 * @param e
	 * @return
	 */
	public static int i(String tag, String msg, Throwable e) 
	{
		if (isLoggingEnabled)
		{
			return Log.i(tag, msg, e);
		}
		return 0;
	}

	/**
	 * Send a INFO log message and log the exception.
	 * @param tag
	 * @param format
	 * @param e
	 * @param args
	 * @return
	 */
	public static int i(String tag, String format, Throwable e, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.i(tag, format(format, args), e);
		}
		return 0;
	}

	/**
	 * Send a ERROR log message.
	 * @param tag
	 * @param format
	 * @param args
	 * @return
	 */
	public static int e(String tag, String format, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.e(tag, format(format, args));
		}
		return 0;
	}

	/**
	 * Send a ERROR log message and log the exception.
	 * @param tag
	 * @param msg
	 * @param e
	 * @return
	 */
	public static int e(String tag, String msg, Throwable e) 
	{
		if (isLoggingEnabled)
		{
			return Log.e(tag, msg, e);
		}
		return 0;
	}

	/**
	 * Send a ERROR log message and log the exception.
	 * @param tag
	 * @param format
	 * @param e
	 * @param args
	 * @return
	 */
	public static int e(String tag, String format, Throwable e, Object... args) 
	{
		if (isLoggingEnabled)
		{
			return Log.e(tag, format(format, args), e);
		}
		return 0;
	}

	private static String format(String format, Object... args) 
	{
		try  {
			return String.format(format, args);
		} 
		catch (NullPointerException exp) {
			LogWrapper.w(TAG, "Message is Null. reason=%s", exp.getMessage());
			return String.format(EMPTY, format);
		}
		catch (Exception e) {
			LogWrapper.e(TAG, "error. reason=%s, format=%s", e.getMessage(), format);
			return String.format(EMPTY, format);
		}
	}
}
