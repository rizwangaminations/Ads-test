//
//  IListening.h
//  ModuleSpecialOffer
//
//  Created by Serhii Tkach on 19/04/2016.
//

#ifndef IListening_h
#define IListening_h

#include <vector>
#include <functional>

template <typename _TListener_>
class IListening
{
public:
    typedef typename std::function<void(_TListener_*)> ListenerFunctor;
    
    //NOTE: add listeners
    void addListener(_TListener_* pListener)
    {
        //NOTE: check if listener is already registered
        for (typename ListenersArray::iterator it = this->m_listeners.begin(); it != this->m_listeners.end(); ++it)
        {
            if( (*it) == pListener )
            {
                return;
            }
        }
        this->m_listeners.push_back(pListener);
    }

    //NOTE: remove listeners
    void removeListener(_TListener_* pListener)
    {
        //NOTE: find and remove listener
        for (typename ListenersArray::iterator it = this->m_listeners.begin(); it != this->m_listeners.end(); ++it)
        {
            if( ( *it ) == pListener )
            {
                this->m_listeners.erase(it);
                return;
            }
        }
    }

    //NOTE: iterate over listeners
    void for_each_listener(ListenerFunctor func)
    {
        const auto listenersCopy = this->m_listeners;
        if (func != nullptr)
        {
            for (typename ListenersArray::const_iterator it = listenersCopy.begin(); it != listenersCopy.end(); ++it)
            {
                if ((*it) != nullptr)
                {
                    func(*it);
                }
            }
        }
    }
    
private:
    typedef typename std::vector<_TListener_*> ListenersArray;
    ListenersArray	m_listeners;
};

#endif //IListening_h