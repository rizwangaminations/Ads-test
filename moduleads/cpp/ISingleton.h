#ifndef _ISingleton_h__
#define _ISingleton_h__

#include "cocos2d.h"
#include "module-analytics-include.h"


template <typename T>
class ISingleton
{
public:
	static T* getInstance()
	{
		if (s_instance == nullptr)
		{
			s_instance = new T();

		}
		return s_instance;
	}
	
	static void deleteInstance()
	{
		if (s_instance != nullptr)
		{
			delete s_instance;
			s_instance = nullptr;
		}
	}

protected:
	ISingleton() {}
	virtual ~ISingleton() {}
	
	ISingleton(const ISingleton& rhs); //disable copy constructor
	ISingleton(ISingleton&& rhs); //disable move constructor

private:
	static T* s_instance;
};

template <typename T>
T* ISingleton<T>::s_instance = nullptr;

#endif //_ISingleton_h__
