//
//  DataEncryptor.h
//  cocos2d_libs
//
//  Created by RizwanAli on 04/04/2023.
//

#ifndef DataEncryptor_h
#define DataEncryptor_h

#include "platform/CCPlatformMacros.h"

NS_CC_BEGIN

class DataEncryptor {
    
private:
    std::string encryptAES(const std::string& plaintext);
    std::string decryptAES(const std::string& ciphertext);
public:
    DataEncryptor(const std::string key, const std::string iv);
    std::string decrypt(const std::string& encrypted_data);
    std::string encrypt(const std::string& plaintext);

private:
    std::string m_key;
    std::string m_iv;
};

NS_CC_END
#endif /* DataEncryptor_h */
